from ...tools.base import BaseTool, ToolMetadata, ToolParameter

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
            return_type="dict"
        )
    
    async def execute(self, **kwargs) -> dict:
        print(f"Scheduling meeting: {kwargs['title']}")
        return {"status": "scheduled", "meeting_id": "123"} 