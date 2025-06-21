#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🌍 Travel Assistant - Complete Startup"
echo "================================================"
echo "📁 Working directory: $(pwd)"
echo ""

# Check if we're in the correct directory
if [[ ! -f "app.py" ]] || [[ ! -f "api.py" ]] || [[ ! -d "orchestrator_agent" ]]; then
    echo "❌ Error: Not in the correct directory. Please run this script from the 14-travel-assistant-agent folder."
    echo "Current directory: $(pwd)"
    echo "Expected files: app.py, api.py, orchestrator_agent/"
    exit 1
fi

echo "✅ Confirmed: Running from correct directory"
echo ""

# Function to check if a port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "❌ Port $port is already in use"
        return 1
    else
        echo "✅ Port $port is available"
        return 0
    fi
}

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [[ -n "$pids" ]]; then
        echo "🔄 Killing processes on port $port: $pids"
        kill -9 $pids 2>/dev/null
        sleep 2
    fi
}

# Check and kill existing processes
echo "🔍 Checking for existing processes..."
kill_port 8000
kill_port 8080
kill_port 8501
echo ""

# Check port availability
echo "🔍 Checking port availability..."
if ! check_port 8000; then exit 1; fi
if ! check_port 8080; then exit 1; fi
if ! check_port 8501; then exit 1; fi
echo ""

# Start ADK Web Server
echo "🚀 Starting ADK Web Server on port 8000..."
python adk_web_server.py > adk_web.log 2>&1 &
ADK_PID=$!
echo "⏳ Waiting for ADK server to initialize..."
sleep 5

# Check if ADK server started successfully
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Failed to start ADK server"
    exit 1
fi
echo "✅ ADK Web Server started (PID: $ADK_PID)"
echo ""

# Start FastAPI Server
echo "🚀 Starting FastAPI Server on port 8080..."
python -m uvicorn api:app --host 0.0.0.0 --port 8080 > fastapi.log 2>&1 &
API_PID=$!
echo "⏳ Waiting for API server to initialize..."
sleep 3

# Check if API server started successfully
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "❌ Failed to start API server"
    exit 1
fi
echo "✅ FastAPI Server started (PID: $API_PID)"
echo ""

# Start Streamlit App
echo "🚀 Starting Streamlit App on port 8501..."
streamlit run app.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &
STREAMLIT_PID=$!
echo "⏳ Waiting for Streamlit to initialize..."
sleep 5

# Check if Streamlit started successfully
if ! curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo "❌ Failed to start Streamlit app"
    exit 1
fi
echo "✅ Streamlit App started (PID: $STREAMLIT_PID)"
echo ""

echo "🎉 All services started successfully!"
echo "📱 Services running:"
echo "   • ADK Web Server: http://localhost:8000"
echo "   • FastAPI Server: http://localhost:8080"
echo "   • Streamlit App: http://localhost:8501"
echo ""
echo "🧪 Test the backend:"
echo "   python simple_test.py"
echo ""
echo "💡 Press Ctrl+C to stop all services"
echo "================================================"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down all services..."
    kill $ADK_PID $API_PID $STREAMLIT_PID 2>/dev/null
    kill_port 8000
    kill_port 8080
    kill_port 8501
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "🔄 Services are running. Press Ctrl+C to stop..."
while true; do
    sleep 1
done