# 🌍 Travel Assistant - Setup Instructions

This guide will help you run the Travel Assistant application with FastAPI and ADK web integration.

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)
```bash
./start.sh
```

### Option 2: Manual startup
```bash
# Install dependencies
pip install -r requirements.txt

# Start all services
python start_services.py
```

## 📋 Prerequisites

- Python 3.8 or higher
- Google ADK installed and configured
- Internet connection for weather and map APIs

## 🔧 What gets started

The startup script will launch three services:

1. **ADK Web Server** (Port 8000)
   - Serves the orchestrator agent through ADK web interface
   - Handles agent interactions and session management

2. **FastAPI Server** (Port 8080)
   - Provides REST API endpoints for the Streamlit frontend
   - Bridges communication between Streamlit and ADK

3. **Streamlit App** (Port 8501)
   - Beautiful web interface for the travel assistant
   - Real-time chat interface with the AI agent

## 🌐 Access Points

Once all services are running, you can access:

- **Main Interface**: http://localhost:8501
- **ADK Web Server**: http://localhost:8000
- **FastAPI Documentation**: http://localhost:8080/docs

## 🎯 Features Available

The Travel Assistant includes:

- **Weather Information**: Real-time weather for any city
- **Tourist Spots**: Top attractions and hidden gems
- **Walking Routes**: Custom walking tours with Google Maps integration
- **Restaurant Recommendations**: Local cuisine suggestions
- **Travel Blog Writing**: AI-generated travel stories
- **Photo Stories**: Narratives based on photos
- **Current Time**: Timezone information for any location

## 🛠️ Troubleshooting

### Port already in use
If you see "Port XXXX is already in use" errors:
```bash
# Find processes using the ports
lsof -i :8000  # ADK Web Server
lsof -i :8080  # FastAPI
lsof -i :8501  # Streamlit

# Kill the processes
kill -9 <PID>
```

### ADK not found
Make sure Google ADK is properly installed:
```bash
pip install google-adk
```

### Dependencies missing
Install all required packages:
```bash
pip install -r requirements.txt
```

## 🔄 Stopping Services

Press `Ctrl+C` in the terminal where you ran the startup script to stop all services gracefully.

## 📝 Manual Service Startup

If you prefer to start services individually:

### 1. Start ADK Web Server
```bash
python adk_web_server.py
```

### 2. Start FastAPI Server (in new terminal)
```bash
uvicorn api:app --host 0.0.0.0 --port 8080
```

### 3. Start Streamlit App (in new terminal)
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🎉 Ready to Travel!

Once everything is running, open http://localhost:8501 in your browser and start planning your next adventure! 🌍✈️ 