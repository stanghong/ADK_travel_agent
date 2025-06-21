#!/bin/bash

# Script to start full Docker setup (ADK server + backend + frontend)
set -e

echo "🚀 Starting Full Travel Assistant Docker Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found! Please create one with your API keys."
    echo "Required environment variables:"
    echo "  - GOOGLE_AI_API_KEY"
    echo "  - GOOGLE_API_KEY"
    echo "  - OPENWEATHER_API_KEY"
    exit 1
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build all images
print_status "Building Docker images..."
docker-compose build

if [ $? -ne 0 ]; then
    print_error "Failed to build Docker images"
    exit 1
fi

print_success "All Docker images built successfully"

# Start all services
print_status "Starting all services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 20

# Check container status
print_status "Checking container status..."
if docker-compose ps | grep -q "Up"; then
    print_success "All containers are running"
else
    print_error "Some containers failed to start"
    docker-compose logs
    exit 1
fi

# Wait for ADK server health check
print_status "Waiting for ADK server health check..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:8000/dev-ui/ >/dev/null 2>&1; then
        print_success "ADK server is healthy!"
        break
    fi
    
    attempt=$((attempt + 1))
    print_status "ADK health check attempt $attempt/$max_attempts..."
    sleep 10
done

if [ $attempt -eq $max_attempts ]; then
    print_error "ADK server health check failed"
    print_status "ADK server logs:"
    docker-compose logs adk-server
    exit 1
fi

# Wait for backend health check
print_status "Waiting for backend health check..."
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:8080/health >/dev/null 2>&1; then
        print_success "Backend is healthy!"
        break
    fi
    
    attempt=$((attempt + 1))
    print_status "Backend health check attempt $attempt/$max_attempts..."
    sleep 10
done

if [ $attempt -eq $max_attempts ]; then
    print_error "Backend health check failed"
    print_status "Backend logs:"
    docker-compose logs backend
    exit 1
fi

# Start frontend locally (since it's not in docker-compose)
print_status "Starting frontend locally..."
if ! pgrep -f "streamlit.*app.py" >/dev/null; then
    print_status "Starting Streamlit frontend..."
    nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
    sleep 10
else
    print_warning "Streamlit frontend is already running"
fi

# Wait for frontend to be ready
print_status "Waiting for frontend to be ready..."
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:8501 >/dev/null 2>&1; then
        print_success "Frontend is ready!"
        break
    fi
    
    attempt=$((attempt + 1))
    print_status "Frontend check attempt $attempt/$max_attempts..."
    sleep 5
done

if [ $attempt -eq $max_attempts ]; then
    print_warning "Frontend health check failed, but continuing..."
fi

# Run comprehensive tests
print_status "Running comprehensive tests..."
python test_full_docker_setup.py

if [ $? -eq 0 ]; then
    print_success "All tests passed! Full Docker setup is working correctly."
    
    echo ""
    echo "🎉 Travel Assistant is ready!"
    echo "=" * 50
    echo "🌐 Services available:"
    echo "  - ADK Server: http://localhost:8000"
    echo "  - ADK Dev UI: http://localhost:8000/dev-ui/"
    echo "  - Backend API: http://localhost:8080"
    echo "  - Frontend: http://localhost:8501"
    echo ""
    echo "📋 Useful commands:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Stop services: docker-compose down"
    echo "  - Restart services: docker-compose restart"
    echo "  - Rebuild: docker-compose build"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  - If frontend shows errors, check: tail -f streamlit.log"
    echo "  - If backend fails, check: docker-compose logs backend"
    echo "  - If ADK fails, check: docker-compose logs adk-server"
    
else
    print_error "Some tests failed. Check the output above for details."
    print_status "Container logs:"
    docker-compose logs --tail=50
    exit 1
fi 