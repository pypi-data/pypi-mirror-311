Certainly! Here's the documentation in Markdown format:

---

# AI Task Scheduler API Documentation

## Overview

The AI Task Scheduler API is a powerful tool for scheduling and managing tasks using natural language. It leverages AI to automatically select and execute the appropriate tools based on task descriptions. This API is designed for enterprise-grade applications, offering robust features for task management, health monitoring, and API key management.

## Key Features

- **Natural Language Task Scheduling**: Easily schedule tasks using simple, human-readable descriptions.
- **Automated Tool Selection**: The AI selects the best tool for the job based on the task description.
- **Health Monitoring**: Keep track of system health and performance metrics.
- **Flexible Job Management**: Manage tasks with ease, including scheduling, status checking, and cancellation.
- **Secure API Key Management**: Generate and manage API keys with role-based access control.

## Getting Started

### Prerequisites

- Python 3.9+
- FastAPI
- Supabase
- Anthropic API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-task-scheduler.git
   cd ai-task-scheduler
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in your credentials.

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Task Management

- **Create Task**
  - **Endpoint**: `POST /tasks`
  - **Description**: Schedule a new task using natural language.
  - **Request Body**:
    ```json
    {
      "description": "Send an SMS to +1234567890 tomorrow at 9 AM about the meeting",
      "schedule_time": "2024-03-20T09:00:00Z",
      "tags": ["reminder", "meeting"]
    }
    ```
  - **Response**:
    ```json
    {
      "status": "scheduled",
      "job_id": "task_123abc",
      "scheduled_time": "2024-03-20T09:00:00Z",
      "description": "Send an SMS to +1234567890 tomorrow at 9 AM about the meeting",
      "tags": ["reminder", "meeting"]
    }
    ```

- **Get Task Status**
  - **Endpoint**: `GET /tasks/{job_id}`
  - **Description**: Retrieve the current status and details of a scheduled task.
  - **Response**:
    ```json
    {
      "job_id": "task_123abc",
      "status": "scheduled",
      "scheduled_for": "2024-03-20T09:00:00Z",
      "metadata": {}
    }
    ```

- **Cancel Task**
  - **Endpoint**: `DELETE /tasks/{job_id}`
  - **Description**: Cancel a scheduled task that hasn't started execution.
  - **Response**:
    ```json
    {
      "status": "cancelled",
      "job_id": "task_123abc"
    }
    ```

### System Monitoring

- **Health Check**
  - **Endpoint**: `GET /health`
  - **Description**: Returns detailed system health metrics including scheduler status, resource usage, and component health.
  - **Response**:
    ```json
    {
      "status": "healthy",
      "timestamp": "2024-03-20T09:00:00Z",
      "metrics": {
        "cpu_usage": 20.5,
        "memory_usage": 45.3,
        "disk_usage": 70.1,
        "scheduler": {
          "healthy": true,
          "active_jobs": 5,
          "failed_jobs": 0,
          "last_successful_execution": "2024-03-20T08:00:00Z"
        }
      },
      "version": "1.0.0"
    }
    ```

### Debugging

- **List Registered Tools**
  - **Endpoint**: `GET /debug/tools`
  - **Description**: List all registered tools and their metadata.
  - **Response**:
    ```json
    {
      "tool_count": 3,
      "tools": [
        {
          "name": "SMSTool",
          "type": "SMSTool",
          "metadata": {
            "name": "SMSTool",
            "description": "Tool for sending SMS messages",
            "category": "communication",
            "parameters": [
              {
                "name": "phone_number",
                "type": "string",
                "description": "The recipient's phone number",
                "required": true
              },
              {
                "name": "message",
                "type": "string",
                "description": "The message content",
                "required": true
              }
            ],
            "return_type": "string",
            "version": "1.0.0"
          }
        }
      ]
    }
    ```

## Registering Tools

To register a new tool, follow these steps:

1. **Create a Tool Class**: Inherit from `BaseTool` and implement the required methods.
   ```python
   from llm_scheduler.tools.base import BaseTool, ToolMetadata, ToolParameter

   class MyCustomTool(BaseTool):
       def _get_metadata(self) -> ToolMetadata:
           return ToolMetadata(
               name="MyCustomTool",
               description="A custom tool for demonstration purposes",
               category="utility",
               parameters=[
                   ToolParameter(name="param1", type="string", description="A parameter", required=True)
               ],
               return_type="string"
           )

       async def execute(self, **kwargs) -> str:
           # Implement the tool's functionality here
           return "Execution result"
   ```

2. **Register the Tool**: Add the tool to the `ToolRegistry` in `main.py`.
   ```python
   from my_tools import MyCustomTool

   # Register tools
   tools = [
       SMSTool(),
       CalendarTool(),
       WeatherAlertTool(),
       MyCustomTool()  # Add your custom tool here
   ]

   for tool in tools:
       registry.register_tool(tool)
   ```

## Additional Utilities

Feel free to add more endpoints or utilities as needed. For example, you could add an endpoint to list all scheduled tasks or to retrieve logs for debugging purposes.

---

This documentation should provide a comprehensive overview of your API's capabilities and how to use it effectively. If you have any specific features or utilities you'd like to add, let me know!
