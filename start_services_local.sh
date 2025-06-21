#!/bin/bash

# Start Local Services Script for Travel Assistant
# This script starts the ADK server, backend API, and Streamlit frontend locally

echo "🚀 Starting Travel Assistant Services Locally..."
echo "================================================"

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "GOOGLE_AI_API_KEY=your_google_ai_api_key"
    echo "GOOGLE_API_KEY=your_google_api_key"
    echo "OPENWEATHER_API_KEY=your_openweather_api_key"
    exit 1
fi

# Check ports
echo "🔍 Checking port availability..."
check_port 8000 || echo "  - Port 8000 (ADK Server) is already in use"
check_port 8080 || echo "  - Port 8080 (Backend API) is already in use"
check_port 8501 || echo "  - Port 8501 (Streamlit Frontend) is already in use"

echo ""
echo "📋 Starting services..."

# Start ADK Server
echo "1️⃣ Starting ADK Server on port 8000..."
python adk_web_server.py &
ADK_PID=$!
echo "   ADK Server PID: $ADK_PID"

# Wait for ADK server to start
sleep 5

# Start Backend API
echo "2️⃣ Starting Backend API on port 8080..."
python -m uvicorn api:app --host 0.0.0.0 --port 8080 --reload &
BACKEND_PID=$!
echo "   Backend API PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Start Streamlit Frontend
echo "3️⃣ Starting Streamlit Frontend on port 8501..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
FRONTEND_PID=$!
echo "   Streamlit Frontend PID: $FRONTEND_PID"

# Wait for all services to start
sleep 5

echo ""
echo "✅ All services started!"
echo ""
echo "🌐 Access your application at:"
echo "  - Frontend (Streamlit): http://localhost:8501"
echo "  - Backend API: http://localhost:8080"
echo "  - ADK Server: http://localhost:8000"
echo ""
echo "📊 Service Status:"
echo "  - ADK Server PID: $ADK_PID"
echo "  - Backend API PID: $BACKEND_PID"
echo "  - Frontend PID: $FRONTEND_PID"
echo ""
echo "🛑 To stop all services, run:"
echo "  kill $ADK_PID $BACKEND_PID $FRONTEND_PID"
echo ""
echo "🧪 To test the setup, run:"
echo "  python test_docker_setup.py"
echo ""
echo "📝 Logs will appear in the terminal. Press Ctrl+C to stop all services."
echo ""

# Save PIDs to file for easy cleanup
echo "$ADK_PID $BACKEND_PID $FRONTEND_PID" > .service_pids

# Wait for user to stop
wait 