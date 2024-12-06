from datetime import datetime, timedelta
import asyncio
import pytz
from ..core.scheduler import LLMScheduler, LLMSchedulerConfig
from ..core.tool_registry import ToolRegistry
from ..tools.base import BaseTool, ToolMetadata, ToolParameter
from scheduler import JobSchedulerConfig

# Example tool implementation
class EmailTool(BaseTool):
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="send_email",
            description="Send an email to specified recipient",
            category="communication",
            parameters=[
                ToolParameter(
                    name="to",
                    type="string",
                    description="Recipient email address"
                ),
                ToolParameter(
                    name="subject",
                    type="string",
                    description="Email subject"
                ),
                ToolParameter(
                    name="body",
                    type="string",
                    description="Email body content"
                )
            ],
            return_type="dict",
            example_usage='send_email(to="user@example.com", subject="Hello", body="Hi there!")'
        )
    
    async def execute(self, **kwargs) -> dict:
        # Implement actual email sending logic
        print(f"Sending email to {kwargs['to']}")
        return {"status": "sent", "to": kwargs['to']}

async def main():
    # Setup
    registry = ToolRegistry()
    registry.register_tool(EmailTool())
    
    config = LLMSchedulerConfig(
        scheduler_config=JobSchedulerConfig(
            retry_failed_jobs=True,
            max_retries=3
        ),
        llm_config={
            "model": "gpt-4",
            "api_key": "your-openai-key"
        }
    )
    
    scheduler = LLMScheduler(config=config, tool_registry=registry)
    
    # Schedule a task using natural language
    future_time = datetime.now(pytz.UTC) + timedelta(minutes=5)
    
    job_id = await scheduler.execute_llm_task(
        "Send an email to john@example.com reminding him about tomorrow's meeting",
        schedule_for=future_time
    )
    
    print(f"Scheduled job: {job_id}")

if __name__ == "__main__":
    asyncio.run(main()) 