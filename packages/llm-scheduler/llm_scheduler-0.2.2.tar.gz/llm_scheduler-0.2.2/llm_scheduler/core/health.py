from datetime import datetime, timedelta
import psutil
import asyncio
from .logger import logger
from typing import Dict, Any
from .tool_registry import ToolRegistry

class HealthCheck:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.last_check = datetime.now()
        
    async def check_system_health(self) -> dict:
        """Perform system health check"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Check scheduler health
            scheduler_status = await self._check_scheduler_health()
            
            health_data = {
                "status": "healthy" if all([
                    cpu_percent < 80,
                    memory.percent < 80,
                    disk.percent < 80,
                    scheduler_status.get("healthy", False)
                ]) else "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "cpu_usage": cpu_percent,
                    "memory_usage": memory.percent,
                    "disk_usage": disk.percent,
                    "scheduler": scheduler_status
                }
            }
            
            logger.info(f"Health check completed: {health_data['status']}")
            return health_data
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _check_scheduler_health(self) -> Dict[str, Any]:
        """Check scheduler specific health metrics"""
        try:
            # Get recent jobs
            recent_jobs = await self._get_jobs_by_status("scheduled") or []
            failed_jobs = await self._get_jobs_by_status("failed") or []
            
            # Get last successful job time with fallback
            last_success_time = getattr(
                self.scheduler, 
                'last_successful_job_time', 
                datetime.now() - timedelta(hours=1)
            )
            
            return {
                "healthy": True,
                "active_jobs": len(recent_jobs),
                "failed_jobs": len(failed_jobs),
                "last_successful_execution": last_success_time.isoformat() if last_success_time else None
            }
        except Exception as e:
            logger.error(f"Scheduler health check failed: {str(e)}")
            return {
                "healthy": False,
                "error": str(e)
            }
    
    async def _get_jobs_by_status(self, status: str) -> list:
        """Safely get jobs by status"""
        try:
            if hasattr(self.scheduler, 'get_jobs_by_status'):
                return await self.scheduler.get_jobs_by_status(status)
            return []
        except Exception as e:
            logger.error(f"Failed to get jobs with status {status}: {str(e)}")
            return []
    
    async def check_tool_registry(self, registry: ToolRegistry) -> Dict[str, Any]:
        """Check tool registry health"""
        try:
            tools = registry.list_tools()
            return {
                "status": "healthy",
                "tool_count": len(tools),
                "tools": [tool.metadata.name for tool in tools]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }