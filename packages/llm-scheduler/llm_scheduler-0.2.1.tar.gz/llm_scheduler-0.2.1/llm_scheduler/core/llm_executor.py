from typing import Dict, Any
import json
import anthropic
from loguru import logger
import traceback

from .tool_registry import ToolRegistry
from ..tools.base import ScheduledToolCall

class LLMExecutor:
    def __init__(self, tool_registry: ToolRegistry, api_key: str, model: str, provider: str = "anthropic", **kwargs):
        self.tool_registry = tool_registry
        self.api_key = api_key
        self.model = model
        self.provider = provider
        self.client = anthropic.Anthropic(api_key=api_key)
        self.max_tokens = kwargs.get('max_tokens', 1024)
        logger.info(f"Initialized LLMExecutor with {provider} provider and model {model}")

    async def plan_execution(self, task_description: str) -> ScheduledToolCall:
        """Use LLM to determine appropriate tool and parameters for a task"""
        try:
            # Create the message using Anthropic's client
            response = await self._get_completion(task_description)
            
            # Debug log the raw response
            logger.debug(f"Raw LLM Response: {response}")
            
            # Check if the response is empty
            if not response:
                raise ValueError("Received empty response from LLM")
            
            # Parse the response and create a ScheduledToolCall
            tool_call = self._parse_llm_response(response)
            return tool_call
            
        except Exception as e:
            logger.error(f"Failed to plan execution: {str(e)}\n{traceback.format_exc()}")
            raise

    async def _get_completion(self, task_description: str) -> str:
        """Get completion from Anthropic's Claude"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{
                    "role": "user",
                    "content": self._create_prompt(task_description)
                }],
                system="You are a task planning assistant. Your job is to analyze tasks and select appropriate tools to execute them. Always respond in valid JSON format."
            )
            
            # Debug log the response
            logger.debug(f"LLM Response: {response.content[0].text}")
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Failed to get completion: {str(e)}")
            logger.error(f"Full error: {traceback.format_exc()}")
            raise

    def _create_prompt(self, task_description: str) -> str:
        """Create a prompt for the LLM"""
        available_tools = self.tool_registry.list_tools()
        
        if not available_tools:
            logger.error("No tools registered in ToolRegistry")
            raise ValueError("No tools available for task execution")
        
        # Debug logging
        logger.debug(f"Creating prompt with {len(available_tools)} tools")
        for tool in available_tools:
            logger.debug(f"Tool: {tool.metadata.name} ({type(tool).__name__})")
        
        try:
            tool_descriptions = "\n".join([
                f"- {tool.metadata.name}: {tool.metadata.description}"
                for tool in available_tools
            ])
            
            # Add parameter details for each tool
            tool_details = []
            for tool in available_tools:
                params = "\n    ".join([
                    f"- {param.name} ({param.type}): {param.description}"
                    for param in tool.metadata.parameters
                ])
                tool_details.append(f"""
{tool.metadata.name}:
  Description: {tool.metadata.description}
  Parameters:
    {params}""")
            
            return f"""Analyze this task and select the most appropriate tool: "{task_description}"

Available tools:
{tool_descriptions}

Detailed tool information:
{''.join(tool_details)}

You must respond with a valid JSON object containing:
1. tool_name: The name of the selected tool
2. parameters: The parameters required by the tool
3. schedule_type: Either "once" or "recurring"
4. schedule_params: Any scheduling parameters

Example response format:
{{
    "tool_name": "sms_tool",
    "parameters": {{
        "phone_number": "+1234567890",
        "message": "Your appointment reminder"
    }},
    "schedule_type": "once",
    "schedule_params": {{}}
}}

Respond only with the JSON object, no other text."""

        except AttributeError as e:
            logger.error(f"Tool metadata access error: {str(e)}")
            logger.error("Tool instances:")
            for tool in available_tools:
                logger.error(f"  {type(tool).__name__}: {dir(tool)}")
            raise ValueError("Invalid tool configuration") from e

    def _parse_llm_response(self, response: str) -> ScheduledToolCall:
        """Parse LLM response into a ScheduledToolCall"""
        try:
            # Extract JSON from response
            response_json = json.loads(response)
            
            # Validate tool exists
            if not self.tool_registry.get_tool(response_json["tool_name"]):
                raise ValueError(f"Selected tool '{response_json['tool_name']}' not found")
            
            return ScheduledToolCall(
                tool_name=response_json["tool_name"],
                parameters=response_json["parameters"],
                schedule_type=response_json.get("schedule_type", "once"),
                schedule_params=response_json.get("schedule_params", {})
            )
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {str(e)}")
            logger.error(f"Response was: {response}")
            raise ValueError(f"Invalid LLM response format: {str(e)}")