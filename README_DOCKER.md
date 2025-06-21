# Travel Assistant - Docker Deployment Guide

This guide will help you deploy the Travel Assistant application using Docker containers and publish them to Docker Hub.

## 🏗️ Architecture

The application consists of three main components:

1. **ADK Server** (`travel-assistant-adk`) - Runs the Google ADK framework with the orchestrator agent
2. **Backend API** (`travel-assistant-backend`) - FastAPI server that handles requests and communicates with ADK
3. **Frontend** (`travel-assistant-frontend`) - Streamlit web interface for user interaction

## 📋 Prerequisites

- Docker and Docker Compose installed
- Docker Hub account
- API keys for:
  - Google AI API
  - Google API (for Places API)
  - OpenWeather API

## 🔧 Setup

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

### 2. Build and Push to Docker Hub

Replace `your-dockerhub-username` with your actual Docker Hub username:

```bash
# Make scripts executable
chmod +x build-and-push.sh
chmod +x deploy.sh

# Build and push all images
./build-and-push.sh your-dockerhub-username
```

This will:
- Build three Docker images:
  - `your-dockerhub-username/travel-assistant-adk:latest`
  - `your-dockerhub-username/travel-assistant-backend:latest`
  - `your-dockerhub-username/travel-assistant-frontend:latest`
- Push them to Docker Hub

### 3. Deploy the Application

```bash
# Deploy using the production docker-compose file
./deploy.sh your-dockerhub-username
```

## 🚀 Manual Deployment

If you prefer to deploy manually:

### Option 1: Using Docker Compose

```bash
# Update the docker-compose.production.yml file with your username
sed -i 's/your-dockerhub-username/YOUR_USERNAME/g' docker-compose.production.yml

# Deploy
docker-compose -f docker-compose.production.yml up -d
```

### Option 2: Individual Containers

```bash
# Pull images
docker pull your-dockerhub-username/travel-assistant-adk:latest
docker pull your-dockerhub-username/travel-assistant-backend:latest
docker pull your-dockerhub-username/travel-assistant-frontend:latest

# Create network
docker network create travel-network

# Run ADK Server
docker run -d \
  --name travel-assistant-adk \
  --network travel-network \
  -p 8000:8000 \
  -e GOOGLE_AI_API_KEY=$GOOGLE_AI_API_KEY \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  -e OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY \
  your-dockerhub-username/travel-assistant-adk:latest

# Run Backend API
docker run -d \
  --name travel-assistant-backend \
  --network travel-network \
  -p 8080:8080 \
  -e ADK_BASE_URL=http://travel-assistant-adk:8000 \
  -e APP_NAME=orchestrator_agent \
  -e USER_ID=traveler \
  your-dockerhub-username/travel-assistant-backend:latest

# Run Frontend
docker run -d \
  --name travel-assistant-frontend \
  --network travel-network \
  -p 8501:8501 \
  -e API_URL=http://travel-assistant-backend:8080 \
  your-dockerhub-username/travel-assistant-frontend:latest
```

## 🌐 Access the Application

Once deployed, you can access:

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:8080
- **ADK Server**: http://localhost:8000

## 📊 Monitoring

### Check Service Status

```bash
# Using docker-compose
docker-compose -f docker-compose.production.yml ps

# Individual containers
docker ps
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.production.yml logs -f

# Individual services
docker logs travel-assistant-adk
docker logs travel-assistant-backend
docker logs travel-assistant-frontend
```

### Health Checks

The containers include health checks that monitor:
- ADK Server: `http://localhost:8000/`
- Backend API: `http://localhost:8080/health`
- Frontend: `http://localhost:8501/_stcore/health`

## 🔄 Updates

To update the application:

```bash
# Pull latest images
docker-compose -f docker-compose.production.yml pull

# Restart services
docker-compose -f docker-compose.production.yml up -d
```

## 🛑 Stopping Services

```bash
# Stop all services
docker-compose -f docker-compose.production.yml down

# Remove containers and networks
docker-compose -f docker-compose.production.yml down --volumes --remove-orphans
```

## 🔧 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000, 8080, and 8501 are available
2. **API key errors**: Verify your `.env` file contains valid API keys
3. **Network issues**: Check that containers can communicate via the `travel-network`

### Debug Commands

```bash
# Check container logs
docker logs <container-name>

# Enter container for debugging
docker exec -it <container-name> /bin/bash

# Check network connectivity
docker network inspect travel-network
```

## 📝 API Documentation

The backend API provides the following endpoints:

- `GET /health` - Health check
- `POST /start_session` - Start a new conversation session
- `POST /send_message` - Send a message to the travel assistant

## 🔐 Security Notes

- The containers run as non-root users for security
- Environment variables are used for sensitive configuration
- Health checks ensure service availability
- Restart policies are configured for reliability

## 📈 Scaling

For production deployment, consider:

- Using a reverse proxy (nginx) for load balancing
- Implementing proper SSL/TLS certificates
- Setting up monitoring and alerting
- Using Docker Swarm or Kubernetes for orchestration
- Implementing proper backup strategies 