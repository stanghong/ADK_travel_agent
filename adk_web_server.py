import asyncio
import uvicorn
import os
import logging
from dotenv import load_dotenv
from google.adk.cli.fast_api import get_fast_api_app
from orchestrator_agent.agent import root_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Disable OpenTelemetry if environment variable is set
if os.getenv('OTEL_PYTHON_DISABLED', 'false').lower() == 'true':
    os.environ['OTEL_PYTHON_DISABLED'] = 'true'
    logger.info("OpenTelemetry disabled via environment variable")

# Get the current directory as the agents directory
agents_dir = os.path.dirname(os.path.abspath(__file__))

try:
    # Create web server using ADK's built-in FastAPI app
    app = get_fast_api_app(
        agents_dir=agents_dir,
        web=True,
    )

    # Register our agent with the app
    app.state.agents = {"orchestrator_agent": root_agent}
    
    logger.info("ADK FastAPI app created successfully")
    
except Exception as e:
    logger.error(f"Error creating ADK FastAPI app: {e}")
    raise

if __name__ == "__main__":
    logger.info("Starting ADK Web Server on http://0.0.0.0:8000")
    logger.info("Travel Assistant Agent is ready!")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Error starting uvicorn server: {e}")
        raise 