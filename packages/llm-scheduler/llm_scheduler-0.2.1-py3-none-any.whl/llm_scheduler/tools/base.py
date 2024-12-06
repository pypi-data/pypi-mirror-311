from typing import Any, Dict, Optional, List, Union
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

class ToolParameter(BaseModel):
    """Definition of a tool parameter"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum_values: Optional[List[Any]] = None

class ToolMetadata(BaseModel):
    """Metadata for a tool"""
    name: str
    description: str
    category: str
    parameters: List[ToolParameter]
    return_type: str
    example_usage: Optional[str] = None
    version: str = "1.0.0"

class BaseTool(ABC):
    """Base class for all tools that can be called by LLMs"""
    
    def __init__(self):
        self.metadata = self._get_metadata()
    
    @abstractmethod
    def _get_metadata(self) -> ToolMetadata:
        """Return the tool's metadata"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters"""
        pass
    
    def describe(self) -> str:
        """Return a string description of the tool for LLM context"""
        params = "\n".join([
            f"- {p.name} ({p.type}): {p.description}" 
            for p in self.metadata.parameters
        ])
        
        return f"""Tool: {self.metadata.name}
Description: {self.metadata.description}
Parameters:
{params}
Returns: {self.metadata.return_type}
"""

class ScheduledToolCall(BaseModel):
    """Represents a scheduled tool execution"""
    tool_name: str
    parameters: Dict[str, Any]
    schedule_type: str = Field(..., description="Type of schedule (once, recurring)")
    schedule_params: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None 