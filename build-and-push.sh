#!/bin/bash

# Build and Push Script for Travel Assistant Docker Images
# Usage: ./build-and-push.sh [your-dockerhub-username]

set -e

# Check if Docker Hub username is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <your-dockerhub-username>"
    echo "Example: $0 johndoe"
    exit 1
fi

DOCKERHUB_USERNAME=$1
VERSION=${2:-latest}

echo "Building and pushing Docker images to Docker Hub..."
echo "Username: $DOCKERHUB_USERNAME"
echo "Version: $VERSION"

# Build ADK Server Image
echo "Building ADK Server image..."
docker build -f Dockerfile.adk.optimized -t $DOCKERHUB_USERNAME/travel-assistant-adk:$VERSION .
docker tag $DOCKERHUB_USERNAME/travel-assistant-adk:$VERSION $DOCKERHUB_USERNAME/travel-assistant-adk:latest

# Build Backend API Image
echo "Building Backend API image..."
docker build -f Dockerfile.backend -t $DOCKERHUB_USERNAME/travel-assistant-backend:$VERSION .
docker tag $DOCKERHUB_USERNAME/travel-assistant-backend:$VERSION $DOCKERHUB_USERNAME/travel-assistant-backend:latest

# Build Frontend Image
echo "Building Frontend image..."
docker build -f Dockerfile.frontend -t $DOCKERHUB_USERNAME/travel-assistant-frontend:$VERSION .
docker tag $DOCKERHUB_USERNAME/travel-assistant-frontend:$VERSION $DOCKERHUB_USERNAME/travel-assistant-frontend:latest

# Push images to Docker Hub
echo "Pushing images to Docker Hub..."

echo "Pushing ADK Server..."
docker push $DOCKERHUB_USERNAME/travel-assistant-adk:$VERSION
docker push $DOCKERHUB_USERNAME/travel-assistant-adk:latest

echo "Pushing Backend API..."
docker push $DOCKERHUB_USERNAME/travel-assistant-backend:$VERSION
docker push $DOCKERHUB_USERNAME/travel-assistant-backend:latest

echo "Pushing Frontend..."
docker push $DOCKERHUB_USERNAME/travel-assistant-frontend:$VERSION
docker push $DOCKERHUB_USERNAME/travel-assistant-frontend:latest

echo "✅ All images built and pushed successfully!"
echo ""
echo "To deploy using docker-compose:"
echo "1. Update docker-compose.production.yml with your Docker Hub username"
echo "2. Run: docker-compose -f docker-compose.production.yml up -d"
echo ""
echo "Or pull and run individual containers:"
echo "docker pull $DOCKERHUB_USERNAME/travel-assistant-adk:latest"
echo "docker pull $DOCKERHUB_USERNAME/travel-assistant-backend:latest"
echo "docker pull $DOCKERHUB_USERNAME/travel-assistant-frontend:latest" 