from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum_values: Optional[List[Any]] = None

class ToolMetadata(BaseModel):
    name: str
    description: str
    category: str
    parameters: List[ToolParameter]
    return_type: str
    example_usage: Optional[str] = None

class ScheduledToolCall(BaseModel):
    """Represents a scheduled tool execution"""
    tool_name: str
    parameters: Dict[str, Any]
    schedule_type: str = "once"  # "once" or "recurring"
    schedule_params: Dict[str, Any] = {}
    metadata: Optional[Dict[str, Any]] = None

class BaseTool(ABC):
    def __init__(self):
        self.metadata = self._get_metadata()
    
    @abstractmethod
    def _get_metadata(self) -> ToolMetadata:
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass 