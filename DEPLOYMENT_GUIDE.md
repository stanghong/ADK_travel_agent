# 🚀 Deployment Guide

This guide covers deploying the Travel Assistant Agent to both local environments and Railway.

## 📋 Prerequisites

### Required
- Python 3.10+
- Git
- Google AI API Key

### Optional
- OpenWeather API Key (for weather features)
- Railway account (for cloud deployment)
- Docker (for containerized deployment)

## 🏠 Local Deployment

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd 14-travel-assistant-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

Required environment variables:
```bash
GOOGLE_API_KEY="your-google-ai-api-key"
OPENWEATHER_API_KEY="your-openweather-api-key"  # Optional
OTEL_PYTHON_DISABLED="true"
PORT=8000
```

### 3. Run the Application

```bash
# Start the server
python adk_server_with_api.py
```

The application will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 4. Test the Deployment

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test session creation
curl -X POST http://localhost:8000/api/start_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser"}'

# Test message sending
curl -X POST http://localhost:8000/api/send_message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "testuser",
    "session_id": "session-123",
    "message": "What is the weather in Paris?"
  }'
```

## 🐳 Docker Deployment

### 1. Build the Image

```bash
# Build using Railway Dockerfile
docker build -f Dockerfile.railway -t travel-assistant .

# Or build using standard Dockerfile
docker build -t travel-assistant .
```

### 2. Run with Docker

```bash
# Run with environment file
docker run -p 8000:8000 --env-file .env travel-assistant

# Or run with environment variables
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY="your-key" \
  -e OPENWEATHER_API_KEY="your-key" \
  -e OTEL_PYTHON_DISABLED="true" \
  travel-assistant
```

### 3. Docker Compose

```bash
# Start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

## ☁️ Railway Deployment

### 1. Prepare for Railway

Ensure your repository is ready:
- ✅ All code is committed to Git
- ✅ `.env.example` file exists
- ✅ `Dockerfile.railway` is present
- ✅ `railway.toml` is configured
- ✅ `.gitignore` excludes `.env`

### 2. Install Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

### 3. Deploy to Railway

#### Option A: Using the Deployment Script

```bash
# Make script executable (if not already)
chmod +x deploy_railway.sh

# Run deployment script
./deploy_railway.sh
```

#### Option B: Manual Deployment

```bash
# Link to Railway project
railway link

# Deploy
railway up

# Get deployment URL
railway status
```

### 4. Configure Environment Variables

After deployment, set environment variables in Railway dashboard:

1. Go to your Railway project dashboard
2. Navigate to **Variables** tab
3. Add the following variables:

```
GOOGLE_API_KEY=your-google-ai-api-key
OPENWEATHER_API_KEY=your-openweather-api-key
OTEL_PYTHON_DISABLED=true
PORT=8000
```

### 5. Test Railway Deployment

```bash
# Get your deployment URL
railway status

# Test health endpoint
curl https://your-app.railway.app/health

# Test API endpoints
curl -X POST https://your-app.railway.app/api/start_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser"}'
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google AI API key | - | Yes |
| `OPENWEATHER_API_KEY` | OpenWeather API key | - | No |
| `OTEL_PYTHON_DISABLED` | Disable OpenTelemetry | "true" | No |
| `PORT` | Server port | 8000 | No |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI | "False" | No |

### Railway-Specific Variables

| Variable | Description | Set By |
|----------|-------------|--------|
| `RAILWAY_DEPLOYMENT_VERSION` | Deployment version | Railway |
| `RAILWAY_PROJECT_ID` | Project identifier | Railway |
| `RAILWAY_SERVICE_ID` | Service identifier | Railway |

## 🧪 Testing Your Deployment

### Health Check

```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "Healthy",
  "adk_server": "Integrated",
  "api_server": "Online"
}
```

### API Testing

```bash
# 1. Start a session
SESSION_RESPONSE=$(curl -s -X POST https://your-app.railway.app/api/start_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser"}')

SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)

# 2. Send a test message
curl -X POST https://your-app.railway.app/api/send_message \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"testuser\",
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"What is the weather in Paris?\"
  }"
```

### Load Testing

```bash
# Simple load test with Apache Bench
ab -n 100 -c 10 https://your-app.railway.app/health

# Or with curl in a loop
for i in {1..10}; do
  curl -s https://your-app.railway.app/health &
done
wait
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use (Local)
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

#### 2. Railway Deployment Fails
```bash
# Check logs
railway logs

# Rebuild and redeploy
railway up --build
```

#### 3. API Key Issues
- Verify your Google AI API key is valid
- Check API key permissions
- Ensure the key is set in Railway dashboard

#### 4. Docker Build Fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -f Dockerfile.railway -t travel-assistant .
```

### Debug Commands

```bash
# Check Railway status
railway status

# View Railway logs
railway logs

# Check environment variables
railway variables

# Test local deployment
python -c "from adk_server_with_api import app; print('App imports successfully')"
```

## 📊 Monitoring

### Railway Dashboard
- Monitor deployment status
- View application logs
- Check resource usage
- Manage environment variables

### Health Monitoring
```bash
# Set up health check monitoring
while true; do
  curl -f https://your-app.railway.app/health || echo "Health check failed"
  sleep 60
done
```

## 🔄 Continuous Deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'
      - run: npm install -g @railway/cli
      - run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## 🎉 Success!

Your Travel Assistant is now deployed and ready to help users plan their trips! 

### Next Steps
1. Share your deployment URL with users
2. Monitor application performance
3. Set up alerts for any issues
4. Consider adding authentication if needed
5. Scale resources as usage grows

---

**Happy Deploying! 🚀** 