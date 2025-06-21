#!/bin/bash

# Activate the virtual environment
source ../.venv/bin/activate

# Function to stop services
stop_services() {
    echo "Stopping all services..."
    pkill -f "python adk_web_server.py"
    pkill -f "python -m uvicorn api:app"
    pkill -f "streamlit run app.py"
    echo "All services stopped."
    exit 0
}

# Set up signal handlers
trap stop_services SIGINT SIGTERM

# Start ADK web server
echo "Starting ADK web server..."
python adk_web_server.py > adk_web.log 2>&1 &
ADK_PID=$!

# Start FastAPI server
echo "Starting FastAPI server..."
python -m uvicorn api:app --host 0.0.0.0 --port 8080 > fastapi.log 2>&1 &
FASTAPI_PID=$!

# Start Streamlit app
echo "Starting Streamlit app..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
STREAMLIT_PID=$!

echo "All services started!"
echo "ADK web:      http://localhost:8000"
echo "FastAPI:      http://localhost:8080"
echo "Streamlit UI: http://localhost:8501"
echo "Press Ctrl+C to stop all services"

# Wait for all background processes
wait 