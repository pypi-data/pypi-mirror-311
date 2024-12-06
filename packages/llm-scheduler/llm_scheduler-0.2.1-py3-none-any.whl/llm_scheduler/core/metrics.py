from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Metrics
SCHEDULED_JOBS = Counter(
    'scheduled_jobs_total',
    'Total number of jobs scheduled',
    ['tool_name', 'status']
)

EXECUTION_TIME = Histogram(
    'job_execution_seconds',
    'Time spent executing jobs',
    ['tool_name'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

ACTIVE_JOBS = Gauge(
    'active_jobs',
    'Number of currently active jobs',
    ['tool_name']
)

class MetricsTracker:
    @staticmethod
    def track_execution_time(tool_name: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    ACTIVE_JOBS.labels(tool_name=tool_name).inc()
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    EXECUTION_TIME.labels(tool_name=tool_name).observe(execution_time)
                    SCHEDULED_JOBS.labels(tool_name=tool_name, status='success').inc()
                    return result
                except Exception as e:
                    SCHEDULED_JOBS.labels(tool_name=tool_name, status='error').inc()
                    raise
                finally:
                    ACTIVE_JOBS.labels(tool_name=tool_name).dec()
            return wrapper
        return decorator 