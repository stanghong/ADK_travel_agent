# 🚀 Travel Assistant Startup Guide

This guide shows you how to start the Travel Assistant from anywhere without worrying about directory navigation.

## Quick Start Options

### Option 1: One-time Setup with Aliases (Recommended)
```bash
# Navigate to the travel assistant directory once
cd /path/to/agent-development-kit-crash-course/14-travel-assistant-agent

# Run the setup script to create convenient aliases
./setup_alias.sh

# Reload your shell profile
source ~/.zshrc  # or ~/.bashrc

# Now you can use these commands from anywhere:
travel          # Start all services
travel-stop     # Stop all services
travel-test     # Run tests
travel-logs     # View logs
```

### Option 2: Direct Script Execution
```bash
# From anywhere, run the launch script
/path/to/agent-development-kit-crash-course/14-travel-assistant-agent/launch.sh
```

### Option 3: Manual Startup (if you prefer)
```bash
# Navigate to the directory
cd /path/to/agent-development-kit-crash-course/14-travel-assistant-agent

# Start all services
./start_all.sh
```

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `launch.sh` | Smart launcher that finds the correct directory | Run from anywhere |
| `start_all.sh` | Complete startup with all services | Run from travel assistant directory |
| `setup_alias.sh` | Creates convenient shell aliases | Run once for setup |
| `start_backend.sh` | Starts only backend services | For backend-only testing |

## Services Started

- **ADK Web Server**: http://localhost:8000
- **FastAPI Server**: http://localhost:8080  
- **Streamlit App**: http://localhost:8501

## Troubleshooting

### Port Already in Use
The scripts automatically check and kill processes using the required ports (8000, 8080, 8501).

### Wrong Directory Error
If you see "Not in the correct directory" error:
1. Make sure you're running from the `14-travel-assistant-agent` folder
2. Check that `app.py`, `api.py`, and `orchestrator_agent/` exist

### Services Not Starting
1. Check the log files: `adk_web.log`, `fastapi.log`, `streamlit.log`
2. Ensure your virtual environment is activated
3. Verify all dependencies are installed: `pip install -r requirements.txt`

## Convenient Commands (after setup)

```bash
travel          # Start all services
travel-start    # Start all services  
travel-stop     # Stop all services
travel-test     # Run backend tests
travel-logs     # View all service logs in real-time
```

## Manual Service Management

```bash
# Start individual services
python adk_web_server.py                    # ADK server
python -m uvicorn api:app --port 8080      # FastAPI server
streamlit run app.py --port 8501           # Streamlit app

# Stop services
pkill -f "adk_web_server.py"
pkill -f "uvicorn api:app"
pkill -f "streamlit run app.py"
```

## Testing

```bash
# Test the backend
python simple_test.py

# Test the full system
python test_adk_api_backend.py
```

## Logs

All services write logs to:
- `adk_web.log` - ADK server logs
- `fastapi.log` - FastAPI server logs  
- `streamlit.log` - Streamlit app logs

View all logs in real-time:
```bash
tail -f adk_web.log fastapi.log streamlit.log
``` 