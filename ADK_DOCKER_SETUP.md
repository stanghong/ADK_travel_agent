# ADK Server Docker Setup Guide

## Overview

This guide covers running the ADK (Agent Development Kit) server in Docker, including fixes for OpenTelemetry context management issues and comprehensive testing.

## Key Improvements Made

### 1. OpenTelemetry Fixes
- **Disabled OpenTelemetry** in Docker environment to prevent context management errors
- Added environment variables to completely disable telemetry:
  ```bash
  OTEL_PYTHON_DISABLED=true
  OTEL_TRACES_SAMPLER=always_off
  OTEL_METRICS_EXPORTER=none
  OTEL_LOGS_EXPORTER=none
  ```

### 2. Enhanced Dockerfile
- Added proper environment configuration
- Implemented non-root user for security
- Improved health checks with better timeouts
- Added proper error handling and logging

### 3. Improved Error Handling
- Enhanced ADK web server with better logging
- Added graceful error handling for OpenTelemetry issues
- Improved container health checks

## Quick Start

### Prerequisites
1. Docker and Docker Compose installed
2. `.env` file with required API keys:
   ```bash
   GOOGLE_AI_API_KEY=your_google_ai_key
   GOOGLE_API_KEY=your_google_api_key
   OPENWEATHER_API_KEY=your_openweather_key
   ```

### Option 1: Start ADK Server Only
```bash
./start_adk_docker.sh
```

### Option 2: Start Full Docker Setup
```bash
./start_full_docker.sh
```

### Option 3: Manual Docker Compose
```bash
# Build and start ADK server
docker-compose build adk-server
docker-compose up -d adk-server

# Test the ADK server
python test_adk_docker.py
```

## Testing

### ADK Server Test
```bash
python test_adk_docker.py
```

### Full System Test
```bash
python test_full_docker_setup.py
```

## Services Available

When running successfully:

- **ADK Server**: http://localhost:8000
- **ADK Dev UI**: http://localhost:8000/dev-ui/
- **Backend API**: http://localhost:8080 (if running full setup)
- **Frontend**: http://localhost:8501 (if running full setup)

## Troubleshooting

### Common Issues

#### 1. OpenTelemetry Context Errors
**Symptoms**: 500 errors when making requests to ADK server
**Solution**: Ensure OpenTelemetry is disabled in Docker environment

#### 2. Health Check Failures
**Symptoms**: Container marked as unhealthy
**Solution**: 
- Check container logs: `docker-compose logs adk-server`
- Verify the `/dev-ui/` endpoint is accessible
- Increase health check timeouts if needed

#### 3. Container Won't Start
**Symptoms**: Container exits immediately
**Solution**:
- Check for missing `.env` file
- Verify API keys are correct
- Check Docker logs: `docker-compose logs adk-server`

### Debugging Commands

```bash
# View container logs
docker-compose logs -f adk-server

# Check container status
docker-compose ps

# Restart ADK server
docker-compose restart adk-server

# Rebuild and restart
docker-compose build adk-server
docker-compose up -d adk-server

# Test health endpoint manually
curl -f http://localhost:8000/dev-ui/

# Test ADK functionality
curl -X POST http://localhost:8000/apps/orchestrator_agent/users/test_user/sessions/test-session
```

## Configuration Files

### Dockerfile.adk
- Optimized for ADK server
- Disables OpenTelemetry
- Includes security improvements
- Better error handling

### docker-compose.yml
- Includes OpenTelemetry environment variables
- Proper health checks
- Service dependencies
- Network configuration

### adk_web_server.py
- Enhanced logging
- OpenTelemetry handling
- Better error reporting
- Improved startup process

## Performance Considerations

### Memory Usage
- ADK server typically uses 200-500MB RAM
- Monitor with: `docker stats travel-assistant-adk`

### Startup Time
- Initial startup: 30-60 seconds
- Subsequent starts: 10-20 seconds
- Health checks: 30-second intervals

### Scaling
- ADK server can handle multiple concurrent requests
- Consider load balancing for high traffic
- Monitor response times in logs

## Security

### Container Security
- Runs as non-root user
- Minimal base image (python:3.10-slim)
- No unnecessary packages installed

### Network Security
- Services communicate over internal Docker network
- External access only on specified ports
- Health checks validate service integrity

## Monitoring

### Health Checks
- Automatic health monitoring every 30 seconds
- Endpoint: `/dev-ui/`
- Timeout: 30 seconds
- Retries: 5 attempts

### Logging
- Structured logging with timestamps
- Error tracking and reporting
- Access logs enabled

### Metrics
- Response time monitoring
- Error rate tracking
- Container resource usage

## Deployment

### Production Considerations
1. Use production Docker Compose file
2. Set up proper logging aggregation
3. Configure monitoring and alerting
4. Implement backup strategies
5. Use secrets management for API keys

### Environment Variables
```bash
# Required
GOOGLE_AI_API_KEY=your_key
GOOGLE_API_KEY=your_key
OPENWEATHER_API_KEY=your_key

# Optional (for production)
OTEL_PYTHON_DISABLED=true
PYTHONUNBUFFERED=1
```

## Support

### Getting Help
1. Check container logs first
2. Run test scripts to isolate issues
3. Verify environment configuration
4. Check Docker and system resources

### Common Commands Reference
```bash
# Start services
./start_adk_docker.sh
./start_full_docker.sh

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Test functionality
python test_adk_docker.py
python test_full_docker_setup.py

# Rebuild
docker-compose build

# Restart
docker-compose restart
```

## Conclusion

The ADK server now runs reliably in Docker with:
- ✅ OpenTelemetry issues resolved
- ✅ Proper error handling and logging
- ✅ Comprehensive testing suite
- ✅ Security improvements
- ✅ Production-ready configuration

The setup provides a robust foundation for running the travel assistant agent in containerized environments. 