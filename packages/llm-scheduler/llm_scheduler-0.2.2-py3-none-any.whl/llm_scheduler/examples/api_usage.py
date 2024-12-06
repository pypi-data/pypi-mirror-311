from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pytz
from typing import Optional, List

from ..core.scheduler import LLMScheduler, LLMSchedulerConfig
from ..core.tool_registry import ToolRegistry
from ..tools.base import BaseTool, ToolMetadata, ToolParameter
from scheduler import JobSchedulerConfig

app = FastAPI()

# Initialize scheduler (in practice, you might want to use dependency injection)
registry = ToolRegistry()
# Register your tools here...

scheduler = LLMScheduler(
    config=LLMSchedulerConfig(
        scheduler_config=JobSchedulerConfig(retry_failed_jobs=True),
        llm_config={"model": "gpt-4", "api_key": "your-openai-key"}
    ),
    tool_registry=registry
)

class TaskRequest(BaseModel):
    description: str
    schedule_time: Optional[datetime] = None
    priority: Optional[str] = "normal"
    tags: Optional[List[str]] = []

@app.post("/tasks/schedule")
async def schedule_task(request: TaskRequest):
    try:
        job_id = await scheduler.execute_llm_task(
            task_description=request.description,
            schedule_for=request.schedule_time
        )
        
        return {
            "status": "scheduled",
            "job_id": job_id,
            "scheduled_time": request.schedule_time,
            "priority": request.priority
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{job_id}")
async def get_task_status(job_id: str):
    job = scheduler.scheduler.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "job_id": job.job_id,
        "status": job.status,
        "scheduled_for": job.run_date,
        "metadata": job.metadata
    }

# Example usage with curl:
"""
# Schedule a task
curl -X POST http://localhost:8000/tasks/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Send a reminder email to team@example.com about the project deadline",
    "schedule_time": "2024-03-01T14:00:00Z",
    "priority": "high",
    "tags": ["project", "deadline"]
  }'

# Check task status
curl http://localhost:8000/tasks/job_123456
""" 