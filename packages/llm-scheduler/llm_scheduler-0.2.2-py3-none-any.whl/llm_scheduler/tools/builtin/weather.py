from ...tools.base import BaseTool, ToolMetadata, ToolParameter

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