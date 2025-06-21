#!/bin/bash

# Script to build and run ADK server in Docker
set -e

echo "🚀 Starting ADK Server in Docker..."

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

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build the ADK server image
print_status "Building ADK server Docker image..."
docker-compose build adk-server

if [ $? -ne 0 ]; then
    print_error "Failed to build ADK server image"
    exit 1
fi

print_success "ADK server image built successfully"

# Start only the ADK server
print_status "Starting ADK server container..."
docker-compose up -d adk-server

# Wait for the container to be ready
print_status "Waiting for ADK server to be ready..."
sleep 10

# Check container status
print_status "Checking container status..."
if docker-compose ps adk-server | grep -q "Up"; then
    print_success "ADK server container is running"
else
    print_error "ADK server container failed to start"
    docker-compose logs adk-server
    exit 1
fi

# Wait for health check to pass
print_status "Waiting for health check to pass..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:8000/dev-ui/ >/dev/null 2>&1; then
        print_success "ADK server is healthy and ready!"
        break
    fi
    
    attempt=$((attempt + 1))
    print_status "Health check attempt $attempt/$max_attempts..."
    sleep 10
done

if [ $attempt -eq $max_attempts ]; then
    print_error "ADK server health check failed after $max_attempts attempts"
    print_status "Container logs:"
    docker-compose logs adk-server
    exit 1
fi

# Test the ADK server
print_status "Testing ADK server functionality..."
python test_adk_docker.py

if [ $? -eq 0 ]; then
    print_success "ADK server is working correctly in Docker!"
    echo ""
    echo "🌐 ADK Server is available at: http://localhost:8000"
    echo "🔧 Dev UI is available at: http://localhost:8000/dev-ui/"
    echo ""
    echo "To stop the server: docker-compose down"
    echo "To view logs: docker-compose logs -f adk-server"
else
    print_error "ADK server test failed"
    print_status "Container logs:"
    docker-compose logs adk-server
    exit 1
fi 