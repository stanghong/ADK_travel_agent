# 🚀 Travel Assistant Agent

A sophisticated travel planning assistant powered by Google ADK (Agent Development Kit) with multiple specialized sub-agents for comprehensive travel recommendations.

## 🌟 Features

- **🤖 Multi-Agent Architecture**: Orchestrator agent that routes requests to specialized sub-agents
- **🌤️ Real-time Weather**: Get current weather conditions for any destination
- **🏛️ Tourist Attractions**: Discover top attractions and hidden gems
- **🍽️ Restaurant Recommendations**: Find the best dining spots
- **🚶 Walking Routes**: Get walking directions between attractions
- **📝 Travel Blog Writing**: Generate travel blog posts
- **📸 Photo Story Analysis**: Analyze travel photos and provide insights
- **🖼️ Image Search**: Find images of landmarks and attractions
- **⏰ Time Zone Support**: Get current time for any location

## 🏗️ Architecture

```
Travel Assistant
├── Orchestrator Agent (Main Router)
├── Weather Agent (OpenWeather API)
├── Tourist Spots Agent (Travel Recommendations)
├── Restaurant Agent (Dining Recommendations)
├── Walking Routes Agent (Navigation)
├── Blog Writer Agent (Content Generation)
├── Photo Story Agent (Image Analysis)
└── Image Search Agent (Visual Search)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Google AI API Key
- OpenWeather API Key (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd 14-travel-assistant-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   python adk_server_with_api.py
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🐳 Docker Deployment

### Local Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -f Dockerfile.railway -t travel-assistant .
docker run -p 8000:8000 --env-file .env travel-assistant
```

### Railway Deployment

1. **Connect to Railway**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   ```

2. **Deploy to Railway**
   ```bash
   # Link to your Railway project
   railway link
   
   # Deploy
   railway up
   ```

3. **Set environment variables in Railway dashboard**
   - `GOOGLE_API_KEY`: Your Google AI API key
   - `OPENWEATHER_API_KEY`: Your OpenWeather API key
   - `OTEL_PYTHON_DISABLED`: "true"

## 📡 API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `POST /api/start_session` - Start a new chat session
- `POST /api/send_message` - Send a message to the travel assistant

### Example Usage

```bash
# Start a session
curl -X POST http://localhost:8000/api/start_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'

# Send a message
curl -X POST http://localhost:8000/api/send_message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "session_id": "session-123",
    "message": "Help me plan a trip to Paris"
  }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key | Yes |
| `OPENWEATHER_API_KEY` | OpenWeather API key | No |
| `OTEL_PYTHON_DISABLED` | Disable OpenTelemetry | No |
| `PORT` | Server port | No (default: 8000) |

### API Keys Setup

1. **Google AI API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Add to your `.env` file

2. **OpenWeather API Key** (Optional)
   - Visit [OpenWeather](https://openweathermap.org/api)
   - Sign up for a free API key
   - Add to your `.env` file

## 🧪 Testing

### Run Tests
```bash
# Test the API endpoints
python test_adk_endpoints.py

# Test the full application
python test_combined_service.py

# Test Docker deployment
python test_docker_combined.py
```

### Test Examples

```bash
# Test session creation
curl -X POST http://localhost:8000/api/start_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser"}'

# Test weather query
curl -X POST http://localhost:8000/api/send_message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "testuser",
    "session_id": "session-123",
    "message": "What is the weather in Paris?"
  }'
```

## 📁 Project Structure

```
14-travel-assistant-agent/
├── orchestrator_agent/          # Main orchestrator agent
│   ├── agent.py                # Main agent logic
│   └── sub_agents/             # Specialized sub-agents
│       ├── weather_agent/
│       ├── tourist_spots_agent/
│       ├── restaurant_recommendation_agent/
│       ├── walking_routes_agent/
│       ├── blog_writer_agent/
│       ├── photo_story_agent/
│       └── image_search_agent/
├── adk_server_with_api.py      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── Dockerfile.railway          # Railway deployment
├── railway.toml               # Railway configuration
├── docker-compose.yml         # Local Docker setup
└── tests/                     # Test files
```

## 🔍 Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   # Find and kill the process
   lsof -ti:8000 | xargs kill -9
   ```

2. **ADK agent not responding**
   - Check your Google API key is valid
   - Ensure the agent is properly registered
   - Check the logs for error messages

3. **Weather API not working**
   - Verify your OpenWeather API key
   - Check if the API key has the correct permissions

### Logs and Debugging

```bash
# View application logs
tail -f fastapi.log

# Check Docker logs
docker logs <container-id>

# Test individual components
python -c "from orchestrator_agent.agent import root_agent; print('Agent loaded successfully')"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google ADK for the agent development framework
- OpenWeather for weather data
- FastAPI for the web framework
- Railway for deployment platform

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section
- Review the API documentation at `/docs`

---

**Happy Travel Planning! ✈️🌍**
