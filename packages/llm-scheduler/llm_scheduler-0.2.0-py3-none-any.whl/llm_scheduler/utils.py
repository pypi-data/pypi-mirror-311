import asyncio
from typing import Optional
from .core.scheduler import LLMScheduler

def create_scheduler(config: dict, registry: Optional['ToolRegistry'] = None) -> LLMScheduler:
    """Create a scheduler synchronously"""
    async def _create():
        return LLMScheduler(config=config, tool_registry=registry)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_create())
    finally:
        loop.close() 