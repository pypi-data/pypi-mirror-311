from pydantic import BaseModel
from typing import Optional, Dict, Any

class StorageConfig(BaseModel):
    type: str = "sqlite"
    config: Dict[str, Any] = {}

class LLMSchedulerConfig(BaseModel):
    scheduler_config: Dict[str, Any]
    llm_config: Dict[str, Any]
    storage: StorageConfig = StorageConfig()
    max_tokens: int = 1000
    temperature: float = 0.7
    retry_on_error: bool = True
    max_retries: int = 3 