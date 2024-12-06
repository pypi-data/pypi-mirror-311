from typing import Dict, List, Optional
from ..tools.base import BaseTool
from loguru import logger

class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        logger.info("Initialized ToolRegistry")
    
    def register_tool(self, tool: BaseTool) -> None:
        """Register a new tool"""
        if not isinstance(tool, BaseTool):
            raise TypeError(f"Tool must be an instance of BaseTool, got {type(tool)}")
        
        tool_name = tool.metadata.name
        if tool_name in self._tools:
            logger.warning(f"Tool {tool_name} already registered, overwriting")
        
        self._tools[tool_name] = tool
        logger.info(f"Registered tool: {tool_name}")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        tool = self._tools.get(name)
        if not tool:
            logger.warning(f"Tool not found: {name}")
        return tool
    
    def list_tools(self) -> List[BaseTool]:
        """List all registered tools"""
        return list(self._tools.values())
    
    @property
    def tools(self) -> Dict[str, BaseTool]:
        """Get all registered tools"""
        return self._tools.copy()