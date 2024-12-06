from typing import List, Dict, Any
from ..tools.base import BaseTool, ToolMetadata, ToolParameter

class EventOrganizerTool(BaseTool):
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="organize_event",
            description="Organize an event with multiple coordinated tasks",
            category="event_management",
            parameters=[
                ToolParameter(
                    name="event_name",
                    type="string",
                    description="Name of the event"
                ),
                ToolParameter(
                    name="date",
                    type="string",
                    description="Event date (ISO format)"
                ),
                ToolParameter(
                    name="attendees",
                    type="list",
                    description="List of attendee contact information"
                ),
                ToolParameter(
                    name="location",
                    type="string",
                    description="Event location"
                ),
                ToolParameter(
                    name="requirements",
                    type="dict",
                    description="Special requirements or preferences",
                    required=False
                )
            ],
            return_type="dict",
            example_usage='organize_event(event_name="Team Building", date="2024-03-15T09:00:00Z", attendees=["john@example.com"])'
        )
    
    async def execute(self, **kwargs) -> dict:
        # This tool coordinates multiple sub-tasks
        tasks = []
        
        # 1. Schedule the main event
        tasks.append({
            "tool": "schedule_meeting",
            "params": {
                "title": kwargs["event_name"],
                "start_time": kwargs["date"],
                "attendees": kwargs["attendees"]
            }
        })
        
        # 2. Send calendar invites
        tasks.append({
            "tool": "send_email",
            "params": {
                "to": kwargs["attendees"],
                "subject": f"Invitation: {kwargs['event_name']}",
                "body": f"You're invited to {kwargs['event_name']} at {kwargs['location']}"
            }
        })
        
        # 3. Schedule reminder notifications
        tasks.append({
            "tool": "send_sms",
            "params": {
                "to_number": "extracted_from_attendees",
                "message": f"Reminder: {kwargs['event_name']} tomorrow"
            }
        })
        
        # 4. Check weather if outdoor event
        if kwargs.get("requirements", {}).get("outdoor", False):
            tasks.append({
                "tool": "weather_alert",
                "params": {
                    "location": kwargs["location"],
                    "alert_type": "rain",
                    "recipients": kwargs["attendees"]
                }
            })
        
        print(f"Organizing event: {kwargs['event_name']}")
        return {
            "status": "organized",
            "event_id": "evt_123",
            "scheduled_tasks": tasks
        } 