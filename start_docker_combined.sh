#!/bin/bash

# Startup script for the combined service Docker container
# This script builds and runs the container with comprehensive testing

set -e  # Exit on any error

echo "🐳 Starting Combined Service Docker Container"
echo "=============================================="

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

# Check if Docker is running
print_status "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi
print_success "Docker is running"

# Stop and remove existing containers
print_status "Cleaning up existing containers..."
docker-compose -f docker-compose.combined.yml down --remove-orphans 2>/dev/null || true
print_success "Cleanup completed"

# Build the Docker image
print_status "Building Docker image..."
docker-compose -f docker-compose.combined.yml build --no-cache
if [ $? -eq 0 ]; then
    print_success "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Start the container
print_status "Starting container..."
docker-compose -f docker-compose.combined.yml up -d
if [ $? -eq 0 ]; then
    print_success "Container started successfully"
else
    print_error "Failed to start container"
    exit 1
fi

# Wait for container to be ready
print_status "Waiting for container to be ready..."
sleep 10

# Check container status
print_status "Checking container status..."
if docker ps | grep -q "travel-assistant-combined"; then
    print_success "Container is running"
else
    print_error "Container is not running"
    docker-compose -f docker-compose.combined.yml logs
    exit 1
fi

# Wait for health check
print_status "Waiting for health check..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Health check passed"
        break
    fi
    attempt=$((attempt + 1))
    print_status "Health check attempt $attempt/$max_attempts..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    print_error "Health check failed after $max_attempts attempts"
    print_status "Container logs:"
    docker-compose -f docker-compose.combined.yml logs
    exit 1
fi

# Run comprehensive tests
print_status "Running comprehensive tests..."
python test_docker_combined.py http://localhost:8000

if [ $? -eq 0 ]; then
    print_success "All tests passed!"
else
    print_error "Some tests failed"
    print_status "Container logs:"
    docker-compose -f docker-compose.combined.yml logs
    exit 1
fi

# Display service information
echo ""
echo "🎉 Combined Service is now running in Docker!"
echo "=============================================="
echo "🌐 Service URL: http://localhost:8000"
echo "🔍 Health Check: http://localhost:8000/health"
echo "🎨 ADK UI: http://localhost:8000/adk/dev-ui/"
echo "📚 API Docs: http://localhost:8000/adk/docs"
echo ""
echo "📋 Available endpoints:"
echo "   GET  /health              - Health check"
echo "   GET  /                    - Root endpoint"
echo "   POST /api/start_session   - Create session"
echo "   POST /api/send_message    - Send message"
echo "   GET  /adk/dev-ui/         - ADK development UI"
echo ""
echo "🔧 Management commands:"
echo "   View logs: docker-compose -f docker-compose.combined.yml logs -f"
echo "   Stop service: docker-compose -f docker-compose.combined.yml down"
echo "   Restart service: docker-compose -f docker-compose.combined.yml restart"
echo ""
print_success "Ready for Railway deployment!" 