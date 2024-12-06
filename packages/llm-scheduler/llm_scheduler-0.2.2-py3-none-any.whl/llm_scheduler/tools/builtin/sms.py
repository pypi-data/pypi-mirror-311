from ...tools.base import BaseTool, ToolMetadata, ToolParameter
from twilio_sms import send_sms

class SMSTool(BaseTool):
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="send_sms",
            description="Send an SMS message to a phone number",
            category="communication",
            parameters=[
                ToolParameter(
                    name="to_number",
                    type="string",
                    description="Recipient phone number (E.164 format)"
                ),
                ToolParameter(
                    name="message",
                    type="string",
                    description="Message content"
                )
            ],
            return_type="dict",
            example_usage='send_sms(to_number="+1234567890", message="Your appointment is confirmed")'
        )
    
    async def execute(self, **kwargs) -> dict:
        # Send SMS using imported send_sms function
        result = send_sms(
            to_number=kwargs['to_number'],
            message=kwargs['message']
        )
        return {"status": "sent", "to": kwargs['to_number'], "result": result} 