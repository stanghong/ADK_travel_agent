#!/bin/bash

# Stop Local Services Script for Travel Assistant

echo "🛑 Stopping Travel Assistant Services..."
echo "========================================"

# Function to kill process by port
kill_by_port() {
    local port=$1
    local service_name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "🔄 Stopping $service_name on port $port..."
        lsof -ti:$port | xargs kill -9
        echo "✅ $service_name stopped"
    else
        echo "ℹ️  $service_name on port $port is not running"
    fi
}

# Kill services by port
kill_by_port 8501 "Streamlit Frontend"
kill_by_port 8080 "Backend API"
kill_by_port 8000 "ADK Server"

# Also try to kill by PIDs if .service_pids file exists
if [ -f .service_pids ]; then
    echo ""
    echo "🔄 Stopping services by PID..."
    pids=$(cat .service_pids)
    for pid in $pids; do
        if kill -0 $pid 2>/dev/null; then
            echo "🔄 Stopping process $pid..."
            kill -9 $pid
        fi
    done
    rm -f .service_pids
fi

echo ""
echo "✅ All services stopped!"
echo ""
echo "�� Cleanup complete." 