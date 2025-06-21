# Travel Assistant Agent - Structure Update

## Changes Made

The folder structure has been adjusted to work properly with the ADK web server. Here are the key changes:

### 1. Import Path Updates
- **Before**: `from agents.orchestrator_agent.agent import root_agent`
- **After**: `from orchestrator_agent.agent import root_agent`

### 2. Files Updated
- `adk_web_server.py` - Updated import path
- `start_all.sh` - Updated to use `python adk_web_server.py` instead of `adk web`
- `start.sh` - Improved service management with signal handling
- All test files (`test_*.py`) - Updated import paths

### 3. Startup Scripts
- `start_all.sh` - Starts all services (ADK web, FastAPI, Streamlit) with manual stop
- `start.sh` - Starts all services with proper signal handling (Ctrl+C to stop)
- `test_adk_web.py` - Test script to verify the structure is working

## How to Use

### Quick Start
```bash
# Test the structure first
python test_adk_web.py

# Start all services
./start_all.sh

# Or start with signal handling
./start.sh

# Start ADK web server only
python adk_web_server.py
```

### Service URLs
- **ADK Web Server**: http://localhost:8000
- **FastAPI Server**: http://localhost:8080
- **Streamlit UI**: http://localhost:8501

### Stopping Services
- If using `start_all.sh`: Press Enter when prompted
- If using `start.sh`: Press Ctrl+C
- Manual stop: `pkill -f "python adk_web_server.py"`

## Structure Overview
```
14-travel-assistant-agent/
├── orchestrator_agent/
│   ├── agent.py                    # Main orchestrator agent
│   └── sub_agents/
│       ├── weather_agent/
│       ├── tourist_spots_agent/
│       ├── blog_writer_agent/
│       ├── walking_routes_agent/
│       ├── restaurant_recommendation_agent/
│       └── photo_story_agent/
├── adk_web_server.py              # ADK web server entry point
├── api.py                         # FastAPI server
├── app.py                         # Streamlit UI
├── start_all.sh                   # Startup script
├── start.sh                       # Startup script with signal handling
├── test_adk_web.py               # Structure test script
└── test_*.py                     # Individual agent tests
```

## Verification
Run the test script to ensure everything is working:
```bash
python test_adk_web.py
```

This will verify that:
- All imports work correctly
- The ADK web server can be imported
- The structure is properly configured

## Troubleshooting
If you encounter import errors:
1. Make sure you're in the correct directory
2. Activate the virtual environment: `source ../.venv/bin/activate`
3. Run the test script: `python test_adk_web.py`
4. Check that all files have the correct import paths 