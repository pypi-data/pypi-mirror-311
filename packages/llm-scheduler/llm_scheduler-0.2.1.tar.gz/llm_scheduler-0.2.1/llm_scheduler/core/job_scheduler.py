from pydantic import BaseModel

class JobSchedulerConfig(BaseModel):
    retry_failed_jobs: bool = True
    max_retries: int = 3
    store_job_results: bool = True
    cleanup_after_days: int = 7 