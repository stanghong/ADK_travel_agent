#!/bin/bash

# Deployment Script for Travel Assistant
# Usage: ./deploy.sh [your-dockerhub-username]

set -e

# Check if Docker Hub username is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <your-dockerhub-username>"
    echo "Example: $0 johndoe"
    exit 1
fi

DOCKERHUB_USERNAME=$1

echo "Deploying Travel Assistant..."
echo "Username: $DOCKERHUB_USERNAME"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "GOOGLE_AI_API_KEY=your_google_ai_api_key"
    echo "GOOGLE_API_KEY=your_google_api_key"
    echo "OPENWEATHER_API_KEY=your_openweather_api_key"
    exit 1
fi

# Update docker-compose.production.yml with the correct username
echo "Updating docker-compose.production.yml with username: $DOCKERHUB_USERNAME"
sed -i.bak "s/your-dockerhub-username/$DOCKERHUB_USERNAME/g" docker-compose.production.yml

# Pull latest images
echo "Pulling latest images from Docker Hub..."
docker-compose -f docker-compose.production.yml pull

# Stop existing containers if running
echo "Stopping existing containers..."
docker-compose -f docker-compose.production.yml down

# Start the services
echo "Starting services..."
docker-compose -f docker-compose.production.yml up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 30

# Check service status
echo "Checking service status..."
docker-compose -f docker-compose.production.yml ps

echo "✅ Deployment completed!"
echo ""
echo "Services are running on:"
echo "  - Frontend (Streamlit): http://localhost:8501"
echo "  - Backend API: http://localhost:8080"
echo "  - ADK Server: http://localhost:8000"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.production.yml logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose -f docker-compose.production.yml down" 