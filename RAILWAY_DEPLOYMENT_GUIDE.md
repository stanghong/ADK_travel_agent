# Railway Deployment Guide - Combined Service

This guide will help you deploy the combined ADK server and API service to Railway as a single endpoint.

## 🚀 Overview

The combined service (`adk_server_with_api.py`) integrates:
- ADK server functionality
- Backend API endpoints
- Session management
- All in a single FastAPI application

## 📁 Files for Railway Deployment

### Required Files:
1. `adk_server_with_api.py` - Combined service
2. `Dockerfile.railway` - Railway-optimized Dockerfile
3. `requirements.txt` - Python dependencies
4. `orchestrator_agent/` - Agent code directory
5. `.env` - Environment variables (if needed)

### Optional Files:
1. `app_railway_combined.py` - Railway-specific frontend
2. `test_combined_railway.py` - Test script

## 🔧 Railway Deployment Steps

### Step 1: Prepare Your Repository

1. **Ensure all files are committed to your repository:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Verify your repository structure:**
   ```
   your-repo/
   ├── adk_server_with_api.py
   ├── Dockerfile.railway
   ├── requirements.txt
   ├── orchestrator_agent/
   │   ├── agent.py
   │   └── sub_agents/
   ├── .env (if needed)
   └── README.md
   ```

### Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app) and sign in**

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure the deployment:**
   - Railway will automatically detect the Dockerfile
   - Set the following environment variables in Railway dashboard:
     ```
     OTEL_PYTHON_DISABLED=true
     PORT=8000
     ```

4. **Deploy:**
   - Railway will build and deploy your service
   - Monitor the build logs for any issues

### Step 3: Configure Environment Variables

In Railway dashboard, go to your service → Variables tab and add:

```env
OTEL_PYTHON_DISABLED=true
PORT=8000
```

### Step 4: Get Your Railway URL

1. **Find your service URL:**
   - Go to your service in Railway dashboard
   - Click on the "Deployments" tab
   - Copy the generated URL (e.g., `https://your-app-name.railway.app`)

2. **Test the deployment:**
   ```bash
   # Test locally
   python test_combined_railway.py
   
   # Test Railway deployment
   python test_combined_railway.py https://your-app-name.railway.app
   ```

## 🧪 Testing Your Deployment

### Test Script Usage:

```bash
# Test local deployment
python test_combined_railway.py

# Test Railway deployment
python test_combined_railway.py https://your-app-name.railway.app
```

### Manual Testing:

1. **Health Check:**
   ```bash
   curl https://your-app-name.railway.app/health
   ```

2. **Start Session:**
   ```bash
   curl -X POST https://your-app-name.railway.app/start_session \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user"}'
   ```

3. **Send Message:**
   ```bash
   curl -X POST https://your-app-name.railway.app/send_message \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Hello! What can you help me with?",
       "session_id": "session-1234567890",
       "user_id": "test_user"
     }'
   ```

## 🌐 Frontend Deployment

### Option 1: Deploy Frontend to Railway (Recommended)

1. **Create a new Railway service for the frontend:**
   - Create a new service in your Railway project
   - Use the following files:
     - `app_railway_combined.py`
     - `requirements.txt` (ensure streamlit is included)

2. **Create a separate Dockerfile for frontend:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY app_railway_combined.py .
   
   EXPOSE 8501
   CMD ["streamlit", "run", "app_railway_combined.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

3. **Set environment variables:**
   ```env
   RAILWAY_BACKEND_URL=https://your-backend-app-name.railway.app
   ```

### Option 2: Run Frontend Locally

```bash
# Set the backend URL
export RAILWAY_BACKEND_URL="https://your-app-name.railway.app"

# Run the frontend
streamlit run app_railway_combined.py --server.port 8501
```

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures:**
   - Check Railway build logs
   - Ensure all dependencies are in `requirements.txt`
   - Verify Dockerfile syntax

2. **Service Not Starting:**
   - Check environment variables
   - Verify port configuration
   - Check application logs in Railway

3. **ADK Integration Issues:**
   - Ensure `OTEL_PYTHON_DISABLED=true` is set
   - Check agent directory structure
   - Verify imports in `adk_server_with_api.py`

4. **Session Management Issues:**
   - Check session storage implementation
   - Verify session ID generation
   - Test session endpoints individually

### Debug Commands:

```bash
# Check Railway logs
railway logs

# Test specific endpoints
curl -v https://your-app-name.railway.app/health
curl -v https://your-app-name.railway.app/

# Check environment variables
railway variables
```

## 📊 Monitoring

### Railway Dashboard:
- Monitor service health
- Check resource usage
- View deployment logs
- Track environment variables

### Health Endpoints:
- `/health` - Service health check
- `/` - Root endpoint with service info
- `/adk/dev-ui/` - ADK development UI

## 🔄 Updates and Redeployment

### Automatic Deployment:
- Railway automatically redeploys when you push to your main branch
- Monitor deployment logs for any issues

### Manual Redeployment:
1. Push changes to your repository
2. Railway will automatically trigger a new deployment
3. Monitor the deployment process

## 🎯 Best Practices

1. **Environment Variables:**
   - Use Railway's environment variable system
   - Never commit sensitive data to your repository
   - Use different variables for different environments

2. **Monitoring:**
   - Set up health checks
   - Monitor resource usage
   - Set up alerts for service failures

3. **Security:**
   - Use HTTPS (Railway provides this automatically)
   - Implement proper session management
   - Validate all inputs

4. **Performance:**
   - Optimize Docker image size
   - Use appropriate resource limits
   - Monitor response times

## 📞 Support

If you encounter issues:

1. Check Railway documentation: https://docs.railway.app
2. Review application logs in Railway dashboard
3. Test endpoints individually
4. Verify environment configuration

## 🎉 Success!

Once deployed, your combined service will be available at:
- **Backend API:** `https://your-app-name.railway.app`
- **ADK UI:** `https://your-app-name.railway.app/adk/dev-ui/`
- **Health Check:** `https://your-app-name.railway.app/health`

Your travel assistant is now ready to help users worldwide! 🌍✈️ 