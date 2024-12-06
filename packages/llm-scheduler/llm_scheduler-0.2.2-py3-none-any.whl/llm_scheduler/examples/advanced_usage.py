from datetime import datetime, timedelta
import asyncio
import pytz
from typing import Optional, Dict, Any
from ..core.scheduler import LLMScheduler, LLMSchedulerConfig
from ..core.tool_registry import ToolRegistry
from ..tools.base import BaseTool, ToolMetadata, ToolParameter
from scheduler import JobSchedulerConfig
# from twilio_sms import send_sms

# # Example Tool Implementations
# class SMSTool(BaseTool):
#     def _get_metadata(self) -> ToolMetadata:
#         return ToolMetadata(
#             name="send_sms",
#             description="Send an SMS message to a phone number",
#             category="communication",
#             parameters=[
#                 ToolParameter(
#                     name="to_number",
#                     type="string",
#                     description="Recipient phone number (E.164 format)"
#                 ),
#                 ToolParameter(
#                     name="message",
#                     type="string",
#                     description="Message content"
#                 )
#             ],
#             return_type="dict",
#             example_usage='send_sms(to_number="+1234567890", message="Your appointment is confirmed")'
#         )
    
#     async def execute(self, **kwargs) -> dict:
#         # Send SMS using imported send_sms function
#         send_sms(
#             to_number=kwargs['to_number'],
#             message=kwargs['message']
#         )
#         print(f"Sending SMS to {kwargs['to_number']}: {kwargs['message']}")
#         return {"status": "sent", "to": kwargs['to_number']}

class CalendarTool(BaseTool):
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="schedule_meeting",
            description="Schedule a meeting in the calendar",
            category="calendar",
            parameters=[
                ToolParameter(
                    name="title",
                    type="string",
                    description="Meeting title"
                ),
                ToolParameter(
                    name="start_time",
                    type="string",
                    description="Meeting start time (ISO format)"
                ),
                ToolParameter(
                    name="duration_minutes",
                    type="integer",
                    description="Meeting duration in minutes",
                    default=30
                ),
                ToolParameter(
                    name="attendees",
                    type="list",
                    description="List of attendee email addresses"
                )
            ],
            return_type="dict",
            example_usage='schedule_meeting(title="Team Sync", start_time="2024-03-01T14:00:00Z", attendees=["user@example.com"])'
        )
    
    async def execute(self, **kwargs) -> dict:
        print(f"Scheduling meeting: {kwargs['title']}")
        return {"status": "scheduled", "meeting_id": "123"}

class WeatherAlertTool(BaseTool):
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="weather_alert",
            description="Send weather alerts based on conditions",
            category="notifications",
            parameters=[
                ToolParameter(
                    name="location",
                    type="string",
                    description="City or coordinates"
                ),
                ToolParameter(
                    name="alert_type",
                    type="string",
                    description="Type of weather alert",
                    enum_values=["rain", "snow", "storm", "heat"]
                ),
                ToolParameter(
                    name="recipients",
                    type="list",
                    description="List of recipient contact info"
                )
            ],
            return_type="dict"
        )
    
    async def execute(self, **kwargs) -> dict:
        print(f"Sending weather alert for {kwargs['location']}")
        return {"status": "sent", "recipients": len(kwargs['recipients'])}

async def example_usage():
    # Setup
    registry = ToolRegistry()
    
    # Register tools
    registry.register_tool(SMSTool())
    registry.register_tool(CalendarTool())
    registry.register_tool(WeatherAlertTool())
    
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
    
    # Example 1: Schedule an immediate SMS notification
    result = await scheduler.execute_llm_task(
        "Send an SMS to +1234567890 letting them know their order #12345 has shipped"
    )
    print("Immediate SMS Result:", result)
    
    # Example 2: Schedule a meeting for tomorrow
    tomorrow = datetime.now(pytz.UTC) + timedelta(days=1)
    meeting_job = await scheduler.execute_llm_task(
        "Schedule a team sync meeting tomorrow at 2 PM with john@example.com and sarah@example.com",
        schedule_for=tomorrow
    )
    print("Scheduled Meeting Job:", meeting_job)
    
    # Example 3: Set up a recurring weather alert
    daily_time = datetime.now(pytz.UTC).replace(hour=8, minute=0)  # 8 AM daily
    weather_job = await scheduler.execute_llm_task(
        "Send daily weather alerts for Seattle to +1234567890 and weather@example.com",
        schedule_for=daily_time
    )
    print("Weather Alert Job:", weather_job)
    
    # Example 4: Complex multi-step task
    event_time = datetime.now(pytz.UTC) + timedelta(days=2)
    complex_job = await scheduler.execute_llm_task(
        f"""
        For the upcoming team offsite on {event_time.strftime('%Y-%m-%d')}:
        1. Schedule a 2-hour meeting
        2. Send calendar invites to team@example.com
        3. Send SMS reminders to all participants 1 hour before
        4. Check weather forecast and alert if rain is expected
        """,
        schedule_for=event_time - timedelta(days=1)  # Prepare one day in advance
    )
    print("Complex Event Job:", complex_job)

if __name__ == "__main__":
    asyncio.run(example_usage()) 