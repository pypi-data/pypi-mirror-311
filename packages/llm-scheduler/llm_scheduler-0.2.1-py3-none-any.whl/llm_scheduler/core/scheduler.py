from typing import Optional, Dict, Any, Union
from datetime import datetime, timedelta
import pytz
from pydantic import BaseModel
import traceback
from functools import wraps
import time
import sys
import re
import asyncio

from ..tools.base.tool import ScheduledToolCall, BaseTool
from .tool_registry import ToolRegistry
from .llm_executor import LLMExecutor
from .storage import get_storage, BaseStorage
from loguru import logger
from .job_scheduler import JobSchedulerConfig
from .types import JobStatus  # Add this import at the top

# Remove default logger and add a new one with DEBUG level
logger.remove()
logger.add(sys.stderr, level="DEBUG")

# Optionally, add a file logger
logger.add("app.log", level="DEBUG", rotation="10 MB")  # Rotate logs every 10 MB

def log_execution_time(func):
    """Decorator to log function execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} completed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}")
            raise
    return wrapper

class LLMSchedulerConfig(BaseModel):
    """Configuration for LLM-enhanced scheduler"""
    scheduler_config: JobSchedulerConfig
    llm_config: Dict[str, Any]
    max_tokens: int = 1000
    temperature: float = 0.7
    retry_on_error: bool = True
    max_retries: int = 3

class LLMScheduler:
    """Enhanced scheduler that handles LLM tool calls"""
    
    def __init__(
        self, 
        config: dict,
        tool_registry: ToolRegistry,
        storage_type: str = "sqlite",
        storage_config: Optional[Dict[str, Any]] = None
    ):
        self.config = config
        self.tool_registry = tool_registry
        self._scheduler = None  # Make scheduler lazy
        
        # Initialize storage
        storage_config = storage_config or {}
        self.storage = get_storage(storage_type, **storage_config)
        
        # Validate API key before initialization
        if not config.get("api_key"):
            raise ValueError("API key is required but not provided")
        
        # Initialize event loop
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        
        try:
            self.llm_executor = LLMExecutor(
                tool_registry=tool_registry,
                **config
            )
            logger.info(f"LLMScheduler initialized with {len(tool_registry.tools)} tools")
        except Exception as e:
            logger.error(f"Failed to initialize LLM Executor: {str(e)}")
            raise
        
        self.timezone = pytz.UTC
    
    @property
    async def scheduler(self):
        """Lazy initialization of scheduler"""
        if self._scheduler is None:
            from scheduler import SupabaseJobScheduler
            self._scheduler = SupabaseJobScheduler()
            await self._scheduler.start()
        return self._scheduler
    
    async def start(self):
        """Start the scheduler"""
        await self.scheduler  # Initialize scheduler
    
    @classmethod
    async def create(cls, config: dict, tool_registry: ToolRegistry, **kwargs):
        """Factory method to create and initialize scheduler"""
        scheduler = cls(config, tool_registry, **kwargs)
        await scheduler.start()
        return scheduler
    
    def _validate_api_key(self):
        """Validate that the API key is working"""
        if not self.llm_executor.api_key:
            raise ValueError("Anthropic API key is not set")
        # You might want to add a test API call here
    
    def _parse_natural_time(self, text: str, base_time: datetime) -> Optional[datetime]:
        """Parse natural language time expressions"""
        try:
            # Common time patterns
            patterns = {
                r'tomorrow at (\d{1,2}):(\d{2})\s*(am|pm)': lambda m: base_time.replace(
                    day=base_time.day + 1,
                    hour=int(m.group(1)) + (12 if m.group(3).lower() == 'pm' and int(m.group(1)) != 12 else 0),
                    minute=int(m.group(2))
                ),
                r'today at (\d{1,2}):(\d{2})\s*(am|pm)': lambda m: base_time.replace(
                    hour=int(m.group(1)) + (12 if m.group(3).lower() == 'pm' and int(m.group(1)) != 12 else 0),
                    minute=int(m.group(2))
                ),
                # Add more patterns as needed
            }
            
            for pattern, handler in patterns.items():
                match = re.search(pattern, text.lower())
                if match:
                    return handler(match)
                    
            return None
            
        except Exception as e:
            logger.error(f"Time parsing failed: {str(e)}")
            return None
            
    @log_execution_time
    async def schedule_tool_call(
        self,
        tool_call: ScheduledToolCall,
        run_at: datetime
    ) -> str:
        """Schedule a tool call for later execution"""
        scheduler_instance = await self.scheduler  # Get initialized scheduler
        
        logger.info(f"Scheduling tool call: {tool_call.tool_name} for {run_at}")
        
        # Validate tool exists
        tool = self.tool_registry.get_tool(tool_call.tool_name)
        if not tool:
            error_msg = f"Tool not found: {tool_call.tool_name}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Create job metadata
        metadata = {
            "created_at": datetime.now(pytz.UTC).isoformat(),
            **(tool_call.metadata or {})
        }
        
        try:
            # Schedule the job
            job = await scheduler_instance.schedule_one_time_job(
                func=self._execute_tool_call,
                run_at=run_at,
                job_id=f"tool_{tool_call.tool_name}_{datetime.now().timestamp()}",
                metadata=metadata,
                tool_call=tool_call.dict()
            )
            
            logger.info(f"Successfully scheduled job {job.job_id} for {run_at}")
            return job.job_id
            
        except Exception as e:
            logger.error(f"Failed to schedule tool call: {str(e)}\n{traceback.format_exc()}")
            raise
    
    @log_execution_time
    async def _execute_tool_call(self, tool_call: Dict[str, Any], **kwargs) -> Any:
        """Execute a tool call (called by scheduler)"""
        tool_call_obj = ScheduledToolCall(**tool_call)
        
        logger.info(f"Executing tool call: {tool_call_obj.tool_name}")
        logger.debug(f"Tool parameters: {tool_call_obj.parameters}")
        
        # Get the tool
        tool = self.tool_registry.get_tool(tool_call_obj.tool_name)
        if not tool:
            error_msg = f"Tool not found: {tool_call_obj.tool_name}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Execute the tool with parameters
        try:
            result = await tool.execute(**tool_call_obj.parameters)
            logger.info(f"Tool execution successful: {tool_call_obj.tool_name}")
            logger.debug(f"Tool result: {result}")
            
            return {
                "status": "success",
                "result": result,
                "tool": tool_call_obj.tool_name
            }
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}\n{traceback.format_exc()}")
            return {
                "status": "error",
                "error": str(e),
                "tool": tool_call_obj.tool_name
            }
    
    @log_execution_time
    async def execute_llm_task(
        self,
        task_description: str,
        schedule_for: Optional[datetime] = None,
        organization_id: Optional[str] = None
    ) -> str:
        """Execute or schedule a task with improved time handling"""
        try:
            # Ensure schedule_for is timezone-aware
            if schedule_for and schedule_for.tzinfo is None:
                schedule_for = pytz.UTC.localize(schedule_for)
                
            # Try to parse natural language time if not explicitly provided
            if not schedule_for:
                base_time = datetime.now(pytz.UTC)
                parsed_time = self._parse_natural_time(task_description, base_time)
                if parsed_time:
                    schedule_for = parsed_time
                    
            # Validate schedule time
            if schedule_for:
                now = datetime.now(pytz.UTC)
                if schedule_for <= now:
                    raise ValueError("Schedule time must be in the future")
                    
                # Add a small buffer for very near-future tasks
                if schedule_for - now < timedelta(minutes=1):
                    schedule_for = now + timedelta(minutes=1)
                    
            # Get tool call from LLM
            tool_call = await self.llm_executor.plan_execution(task_description)
            
            # Add scheduling metadata
            tool_call.metadata = tool_call.metadata or {}
            tool_call.metadata.update({
                "organization_id": organization_id,
                "scheduled_time": schedule_for.isoformat() if schedule_for else None,
                "timezone": "UTC"
            })
            
            # Schedule or execute
            if schedule_for:
                return await self.schedule_tool_call(tool_call, schedule_for)
            else:
                result = await self._execute_tool_call(tool_call.dict())
                return result["job_id"] if isinstance(result, dict) else str(result)
                
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}\n{traceback.format_exc()}")
            raise
    
    async def _store_job_metadata(self, job_id: str, run_date: datetime, metadata: Dict[str, Any]) -> None:
        """Store job metadata in storage"""
        try:
            job_data = {
                'job_id': job_id,
                'run_date': run_date.isoformat(),
                'metadata': metadata,
                'status': 'scheduled',
                'created_at': datetime.now().isoformat()
            }
            
            await self.storage.store_job(job_data)
            logger.info(f"Stored job metadata for {job_id}")
        except Exception as e:
            logger.error(f"Failed to store job metadata: {str(e)}")

    async def _update_job_status(self, job_id: str, status: JobStatus) -> None:
        """Update job status in storage"""
        try:
            await self.storage.update_job_status(job_id, status.value)
            logger.info(f"Updated job status for {job_id} to {status.value}")
        except Exception as e:
            logger.error(f"Failed to update job status: {str(e)}")