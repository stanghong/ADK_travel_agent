# Stateful Multi-Agent Travel Assistant (ADK)

This example demonstrates how to create a stateful multi-agent travel assistant in ADK, using an orchestrator agent that delegates to specialized sub-agents for travel planning, weather, tourist spots, blog writing, walking routes, restaurant recommendations, and photo stories.

## Architecture Overview

The system is built around an **Orchestrator Agent** (LLM) that receives user queries and delegates tasks to sub-agents:

- **Weather Agent**: Gets weather info (calls weather API)
- **Tourist Spots Agent**: Finds top tourist spots (uses Google Search API)
- **Blog Writer Agent**: Generates travel blogs (LLM)
- **Walking Routes Agent**: Maps out walking routes (uses Google Search API)
- **Restaurant Recommendation Agent**: Recommends restaurants (uses Google Search API)
- **Photo Story Agent**: Provides background stories for photos (uses Google Search API)

The orchestrator combines results and generates a comprehensive travel response.

## Project Structure

```
8-stateful-multi-agent_copy/
│
├── customer_service_agent/
│   ├── __init__.py
│   ├── agent.py                # Root agent (now imports orchestrator_agent)
│   └── orchestrator_agent/
│       ├── agent.py            # Orchestrator agent definition
│       └── sub_agents/
│           ├── weather_agent/
│           │   └── agent.py
│           ├── tourist_spots_agent/
│           │   └── agent.py
│           ├── blog_writer_agent/
│           │   └── agent.py
│           ├── walking_routes_agent/
│           │   └── agent.py
│           ├── restaurant_recommendation_agent/
│           │   └── agent.py
│           └── photo_story_agent/
│               └── agent.py
│
├── main.py                     # Application entry point
├── api.py                      # FastAPI backend for chat
├── app.py                      # Streamlit frontend for chat
├── utils.py                    # Helper functions
├── .env                        # Environment variables
└── README.md                   # This documentation
```

## Key Components

### Orchestrator Agent
- Receives user queries
- Decides which sub-agent(s) to delegate to
- Combines results and generates a travel blog or answer

### Sub-Agents
- **Weather Agent**: Calls a weather API for current weather
- **Tourist Spots Agent**: Uses Google Search API to find top places
- **Blog Writer Agent**: Uses LLM to generate travel blogs
- **Walking Routes Agent**: Uses Google Search API to map walking routes
- **Restaurant Recommendation Agent**: Uses Google Search API for food suggestions
- **Photo Story Agent**: Uses Google Search API to provide background stories for photos

### API Integrations
- **Google Search API**: Used by tourist spots, walking routes, restaurant, and photo story agents
- **Weather API**: Used by weather agent

## How It Works

1. **User submits a travel-related query** (e.g., "Plan a day in Paris with food and walking routes")
2. **Orchestrator agent** analyzes the query and delegates subtasks to the appropriate sub-agents
3. **Sub-agents** fetch data from APIs or generate content
4. **Orchestrator agent** combines the results and returns a comprehensive response (e.g., a travel blog)

## Example Usage

1. Start the FastAPI backend:
   ```bash
   uvicorn api:app --reload
   ```
2. Start the Streamlit frontend:
   ```bash
   streamlit run app.py
   ```
3. Open the Streamlit app in your browser, start a session, and chat with the travel assistant!

## Extending the System
- Add your API keys for Google Search and weather APIs in `.env`
- Implement the actual API/tool logic in each sub-agent's `tools` list
- Customize the orchestrator's instruction for your use case

## Example Conversation Flow

- **User**: "What are the top tourist spots in Tokyo and what's the weather like?"
- **Orchestrator**: Delegates to tourist spots agent and weather agent, combines results
- **User**: "Can you write a travel blog about my day in Tokyo with food recommendations?"
- **Orchestrator**: Delegates to blog writer and restaurant recommendation agents, combines into a blog

## Production Considerations
- Use persistent session storage for real deployments
- Add authentication and error handling as needed
- Monitor API usage and costs

## Resources
- [ADK Multi-Agent Systems Documentation](https://google.github.io/adk-docs/agents/multi-agent-systems/)
- [State Management in ADK](https://google.github.io/adk-docs/sessions/state/)
