#!/usr/bin/env python3
"""
Startup script for the Travel Assistant application.
This script starts all necessary services:
1. ADK Web Server (port 8000)
2. FastAPI Server (port 8080)
3. Streamlit App (port 8501)
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def check_port_available(port):
    """Check if a port is available."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def start_adk_server():
    """Start the ADK web server."""
    print("🚀 Starting ADK Web Server on port 8000...")
    if not check_port_available(8000):
        print("❌ Port 8000 is already in use. Please stop any existing services.")
        return None
    
    try:
        process = subprocess.Popen([
            sys.executable, "adk_web_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ ADK Web Server started successfully!")
            return process
        else:
            print("❌ Failed to start ADK Web Server")
            return None
    except Exception as e:
        print(f"❌ Error starting ADK Web Server: {e}")
        return None

def start_fastapi_server():
    """Start the FastAPI server."""
    print("🚀 Starting FastAPI Server on port 8080...")
    if not check_port_available(8080):
        print("❌ Port 8080 is already in use. Please stop any existing services.")
        return None
    
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ FastAPI Server started successfully!")
            return process
        else:
            print("❌ Failed to start FastAPI Server")
            return None
    except Exception as e:
        print(f"❌ Error starting FastAPI Server: {e}")
        return None

def start_streamlit_app():
    """Start the Streamlit app."""
    print("🚀 Starting Streamlit App on port 8501...")
    if not check_port_available(8501):
        print("❌ Port 8501 is already in use. Please stop any existing services.")
        return None
    
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the app to start
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Streamlit App started successfully!")
            return process
        else:
            print("❌ Failed to start Streamlit App")
            return None
    except Exception as e:
        print(f"❌ Error starting Streamlit App: {e}")
        return None

def main():
    """Main function to start all services."""
    print("🌍 Travel Assistant - Starting All Services")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists() or not Path("api.py").exists():
        print("❌ Please run this script from the travel assistant project directory")
        sys.exit(1)
    
    processes = []
    
    try:
        # Start ADK Web Server
        adk_process = start_adk_server()
        if adk_process:
            processes.append(("ADK Web Server", adk_process))
        else:
            print("❌ Cannot continue without ADK Web Server")
            return
        
        # Wait a bit for ADK to fully initialize
        time.sleep(2)
        
        # Start FastAPI Server
        api_process = start_fastapi_server()
        if api_process:
            processes.append(("FastAPI Server", api_process))
        else:
            print("❌ Cannot continue without FastAPI Server")
            return
        
        # Wait a bit for API to fully initialize
        time.sleep(2)
        
        # Start Streamlit App
        streamlit_process = start_streamlit_app()
        if streamlit_process:
            processes.append(("Streamlit App", streamlit_process))
        else:
            print("❌ Cannot continue without Streamlit App")
            return
        
        print("\n" + "=" * 50)
        print("🎉 All services started successfully!")
        print("\n📱 Access your Travel Assistant:")
        print("   • Streamlit UI: http://localhost:8501")
        print("   • ADK Web Server: http://localhost:8000")
        print("   • FastAPI Server: http://localhost:8080")
        print("\n💡 Press Ctrl+C to stop all services")
        print("=" * 50)
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️  {name} force killed")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
        
        print("👋 All services stopped. Goodbye!")

if __name__ == "__main__":
    main() 