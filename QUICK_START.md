# 🚀 Quick Start Guide - Travel Assistant Docker Deployment

Get your Travel Assistant running in Docker in 5 minutes!

## ⚡ Quick Setup

### 1. Prerequisites
- Docker and Docker Compose installed
- Docker Hub account
- API keys ready

### 2. Environment Setup
Create `.env` file:
```bash
GOOGLE_AI_API_KEY=your_google_ai_api_key
GOOGLE_API_KEY=your_google_api_key  
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 3. Build & Deploy (One Command)
```bash
# Replace 'your-username' with your Docker Hub username
./build-and-push.sh your-username && ./deploy.sh your-username
```

### 4. Access Your App
- 🌐 **Frontend**: http://localhost:8501
- 🔧 **Backend API**: http://localhost:8080
- ⚙️ **ADK Server**: http://localhost:8000

## 🧪 Test Your Setup
```bash
python test_docker_setup.py
```

## 📋 What's Included

### Docker Images Created:
- `your-username/travel-assistant-adk:latest` - ADK server with orchestrator agent
- `your-username/travel-assistant-backend:latest` - FastAPI backend
- `your-username/travel-assistant-frontend:latest` - Streamlit frontend

### Features:
- ✅ Multi-container architecture
- ✅ Health checks for all services
- ✅ Non-root user security
- ✅ Automatic restart policies
- ✅ Production-ready configuration
- ✅ Easy scaling and updates

## 🔄 Common Commands

```bash
# View logs
docker-compose -f docker-compose.production.yml logs -f

# Stop services
docker-compose -f docker-compose.production.yml down

# Update to latest version
docker-compose -f docker-compose.production.yml pull && docker-compose -f docker-compose.production.yml up -d

# Check status
docker-compose -f docker-compose.production.yml ps
```

## 🆘 Troubleshooting

### Services not starting?
```bash
# Check logs
docker-compose -f docker-compose.production.yml logs

# Verify .env file exists
ls -la .env

# Check port availability
netstat -tulpn | grep -E ':(8000|8080|8501)'
```

### API key errors?
- Verify all API keys in `.env` file
- Check Google AI API quota
- Ensure OpenWeather API key is valid

## 📚 Next Steps

1. **Customize**: Modify agent behavior in `orchestrator_agent/agent.py`
2. **Scale**: Add load balancer and SSL certificates
3. **Monitor**: Set up logging and monitoring
4. **Deploy**: Push to cloud platform (AWS, GCP, Azure)

## 🎯 Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ADK Server    │
│  (Streamlit)    │◄──►│   (FastAPI)     │◄──►│   (Google ADK)  │
│   Port: 8501    │    │   Port: 8080    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

Ready to deploy! 🚀 