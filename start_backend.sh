#!/bin/bash

# Travel Assistant Backend Startup Script
# This script starts the ADK server and API server

echo "🌍 Travel Assistant - Starting Backend Services"
echo "================================================"

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Check ports
echo "🔍 Checking port availability..."
check_port 8000 || exit 1
check_port 8080 || exit 1

# Start ADK Web Server
echo ""
echo "🚀 Starting ADK Web Server on port 8000..."
python adk_web_server.py &
ADK_PID=$!

# Wait for ADK server to start
echo "⏳ Waiting for ADK server to initialize..."
sleep 5

# Check if ADK server is running
if ! kill -0 $ADK_PID 2>/dev/null; then
    echo "❌ ADK server failed to start"
    exit 1
fi

echo "✅ ADK Web Server started (PID: $ADK_PID)"

# Start FastAPI Server
echo ""
echo "🚀 Starting FastAPI Server on port 8080..."
python -m uvicorn api:app --host 0.0.0.0 --port 8080 &
API_PID=$!

# Wait for API server to start
echo "⏳ Waiting for API server to initialize..."
sleep 3

# Check if API server is running
if ! kill -0 $API_PID 2>/dev/null; then
    echo "❌ API server failed to start"
    kill $ADK_PID 2>/dev/null
    exit 1
fi

echo "✅ FastAPI Server started (PID: $API_PID)"

echo ""
echo "🎉 Backend services started successfully!"
echo ""
echo "📱 Services running:"
echo "   • ADK Web Server: http://localhost:8000"
echo "   • FastAPI Server: http://localhost:8080"
echo ""
echo "🧪 Test the backend:"
echo "   python test_adk_api_backend.py"
echo ""
echo "💡 Press Ctrl+C to stop all services"
echo "================================================"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $ADK_PID 2>/dev/null
    kill $API_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
wait 