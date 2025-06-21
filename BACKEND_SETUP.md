# Travel Assistant - ADK API Backend Setup

This guide explains how to set up and test the Travel Assistant using the ADK API server as a backend.

## Architecture Overview

The Travel Assistant uses a three-tier architecture:

1. **ADK Web Server** (Port 8000) - Runs the Google ADK with the orchestrator agent
2. **FastAPI Server** (Port 8080) - Provides REST API endpoints for the frontend
3. **Streamlit Frontend** (Port 8501) - User interface (optional)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   ADK Web       │
│   Frontend      │◄──►│   Server        │◄──►│   Server        │
│   (Port 8501)   │    │   (Port 8080)   │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### 1. Start Backend Services Only

```bash
# Make the script executable (if not already)
chmod +x start_backend.sh

# Start backend services
./start_backend.sh
```

This will start:
- ADK Web Server on http://localhost:8000
- FastAPI Server on http://localhost:8080

### 2. Test the Backend

```bash
# Run comprehensive test
python test_adk_api_backend.py

# Or run simple test
python simple_test.py
```

### 3. Start Full Application (Optional)

```bash
# Start all services including Streamlit frontend
python start_services.py
```

## API Endpoints

### Health Check
```bash
GET http://localhost:8080/health
```

Response:
```json
{
  "status": "Healthy",
  "adk_server": "Online",
  "api_server": "Online"
}
```

### Start Session
```bash
POST http://localhost:8080/start_session
Content-Type: application/json

{
  "user_id": "traveler"
}
```

Response:
```json
{
  "session_id": "session_123",
  "success": true,
  "message": "Session started successfully"
}
```

### Send Message
```bash
POST http://localhost:8080/send_message
Content-Type: application/json

{
  "session_id": "session_123",
  "message": "What's the weather like in Paris?"
}
```

Response:
```json
{
  "response": "The weather in Paris is currently...",
  "success": true,
  "session_id": "session_123"
}
```

### Get Session Info
```bash
GET http://localhost:8080/session/{session_id}
```

## Testing Examples

### Using curl

```bash
# Health check
curl http://localhost:8080/health

# Start session
curl -X POST http://localhost:8080/start_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Send message (replace SESSION_ID with actual session ID)
curl -X POST http://localhost:8080/send_message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID",
    "message": "What are the top tourist spots in Paris?"
  }'
```

### Using Python

```python
import requests

# Health check
response = requests.get("http://localhost:8080/health")
print(response.json())

# Start session
response = requests.post(
    "http://localhost:8080/start_session",
    json={"user_id": "test_user"}
)
session_id = response.json()["session_id"]

# Send message
response = requests.post(
    "http://localhost:8080/send_message",
    json={
        "session_id": session_id,
        "message": "What's the weather like in Tokyo?"
    }
)
print(response.json()["response"])
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   lsof -i :8080
   
   # Kill the process
   kill -9 <PID>
   ```

2. **ADK server not starting**
   - Check if you have the required dependencies installed
   - Verify the `orchestrator_agent` directory structure
   - Check the logs for specific error messages

3. **API server connection issues**
   - Ensure ADK server is running on port 8000
   - Check if the ADK endpoints are correct
   - Verify the app name and user ID in the API configuration

### Debug Mode

To run with more verbose logging:

```bash
# Start ADK server with debug logging
python adk_web_server.py

# Start API server with debug logging
python -m uvicorn api:app --host 0.0.0.0 --port 8080 --log-level debug
```

### Log Files

The services create log files:
- `adk_web.log` - ADK server logs
- `fastapi.log` - FastAPI server logs
- `streamlit.log` - Streamlit app logs (if used)

## Configuration

The API server configuration is in `api.py`:

```python
class Settings(BaseSettings):
    ADK_BASE_URL: str = "http://localhost:8000"
    APP_NAME: str = "orchestrator_agent"
    USER_ID: str = "traveler"
```

You can override these settings using environment variables:

```bash
export ADK_BASE_URL="http://localhost:8000"
export APP_NAME="orchestrator_agent"
export USER_ID="your_user_id"
```

## Agent Capabilities

The Travel Assistant can help with:

- **Weather Information**: Current weather and forecasts for any location
- **Tourist Spots**: Top attractions and points of interest
- **Walking Routes**: Google Maps walking directions between locations
- **Restaurant Recommendations**: Food suggestions based on location and preferences
- **Blog Writing**: Travel blog generation
- **Photo Stories**: Stories based on photos
- **Current Time**: Time in different timezones

## Development

### Adding New Endpoints

To add new API endpoints, modify `api.py`:

```python
@app.post("/new_endpoint")
async def new_endpoint(request: YourRequestModel):
    # Your implementation here
    pass
```

### Modifying Agent Behavior

To modify the agent's behavior, edit `orchestrator_agent/agent.py`:

```python
root_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.0-flash",
    description="Your description",
    instruction="Your instructions",
    # ... other parameters
)
```

## Support

If you encounter issues:

1. Check the log files for error messages
2. Verify all services are running on the correct ports
3. Test individual components using the provided test scripts
4. Ensure all dependencies are installed correctly 