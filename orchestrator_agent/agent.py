from google.adk.agents import Agent
from .sub_agents.weather_agent.agent import weather_agent
from .sub_agents.tourist_spots_agent.agent import tourist_spots_agent
from .sub_agents.blog_writer_agent.agent import blog_writer_agent
from .sub_agents.walking_routes_agent.agent import walking_routes_agent
from .sub_agents.restaurant_recommendation_agent.agent import restaurant_recommendation_agent
from .sub_agents.photo_story_agent.agent import photo_story_agent
from .sub_agents.image_search_agent.agent import image_search_agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
from datetime import datetime
import pytz
from urllib.parse import quote_plus

def get_current_time(location: str) -> str:
    """
    Get the current time for a specific location.
    
    Args:
        location: The city or timezone name (e.g., "Paris", "New York", "Tokyo")
    
    Returns:
        Current time in the specified location
    """
    try:
        # Common timezone mappings
        timezone_map = {
            "paris": "Europe/Paris",
            "london": "Europe/London",
            "new york": "America/New_York",
            "tokyo": "Asia/Tokyo",
            "sydney": "Australia/Sydney",
            "los angeles": "America/Los_Angeles",
            "chicago": "America/Chicago",
            "mumbai": "Asia/Kolkata",
            "beijing": "Asia/Shanghai",
            "dubai": "Asia/Dubai",
            "moscow": "Europe/Moscow",
            "berlin": "Europe/Berlin",
            "rome": "Europe/Rome",
            "madrid": "Europe/Madrid",
            "amsterdam": "Europe/Amsterdam",
            "vienna": "Europe/Vienna",
            "prague": "Europe/Prague",
            "budapest": "Europe/Budapest",
            "warsaw": "Europe/Warsaw",
            "stockholm": "Europe/Stockholm",
            "oslo": "Europe/Oslo",
            "copenhagen": "Europe/Copenhagen",
            "helsinki": "Europe/Helsinki",
            "riga": "Europe/Riga",
            "tallinn": "Europe/Tallinn",
            "vilnius": "Europe/Vilnius",
            "brussels": "Europe/Brussels",
            "zurich": "Europe/Zurich",
            "geneva": "Europe/Zurich",
            "milan": "Europe/Rome",
            "barcelona": "Europe/Madrid",
            "seville": "Europe/Madrid",
            "valencia": "Europe/Madrid",
            "bilbao": "Europe/Madrid",
            "porto": "Europe/Lisbon",
            "lisbon": "Europe/Lisbon",
            "dublin": "Europe/Dublin",
            "edinburgh": "Europe/London",
            "glasgow": "Europe/London",
            "manchester": "Europe/London",
            "birmingham": "Europe/London",
            "leeds": "Europe/London",
            "liverpool": "Europe/London",
            "newcastle": "Europe/London",
            "cardiff": "Europe/London",
            "belfast": "Europe/London",
            "aberdeen": "Europe/London",
            "dundee": "Europe/London",
            "perth": "Europe/London",
            "stirling": "Europe/London",
            "inverness": "Europe/London",
        }
        
        location_lower = location.lower()
        if location_lower in timezone_map:
            tz_name = timezone_map[location_lower]
        else:
            # Try to find a timezone that contains the location name
            for tz in pytz.all_timezones:
                if location_lower in tz.lower():
                    tz_name = tz
                    break
            else:
                return f"Sorry, I couldn't find timezone information for '{location}'. Please try with a major city name."
        
        tz = pytz.timezone(tz_name)
        current_time = datetime.now(tz)
        return f"Current time in {location}: {current_time.strftime('%I:%M %p, %A, %B %d, %Y')} ({tz_name})"
    
    except Exception as e:
        return f"Error getting time for {location}: {str(e)}"

def get_attraction_image(attraction: str, location: str) -> str:
    """
    Returns a thumbnail image URL for the given attraction and location by searching TripAdvisor.
    """
    # Search TripAdvisor for the attraction and location
    search_query = f"{attraction} {location}"
    encoded_query = quote_plus(search_query)
    
    # TripAdvisor search URL - this will redirect to the attraction page
    tripadvisor_url = f"https://www.tripadvisor.com/Search?q={encoded_query}"
    
    # For now, return a placeholder that indicates TripAdvisor search
    # In a production environment, you would use web scraping or TripAdvisor API
    return f"https://www.tripadvisor.com/Search?q={encoded_query}&searchType=attractions"

current_time_tool = FunctionTool(get_current_time)
get_attraction_image_tool = FunctionTool(get_attraction_image)

# Create AgentTool instances for sub-agents
weather_agent_tool = AgentTool(weather_agent)
tourist_spots_agent_tool = AgentTool(tourist_spots_agent)
walking_routes_agent_tool = AgentTool(walking_routes_agent)
restaurant_agent_tool = AgentTool(restaurant_recommendation_agent)
blog_writer_agent_tool = AgentTool(blog_writer_agent)
photo_story_agent_tool = AgentTool(photo_story_agent)
image_search_agent_tool = AgentTool(image_search_agent)

root_agent = Agent(
    name="orchestrator_agent",
    model="gemini-1.5-flash",
    description="A smart travel assistant that understands conversation context to route to the correct tool.",
    instruction="""
    You are a master orchestrator for a travel agency. Your primary job is to analyze the user's request
    **in the context of the conversation history** and route it to the correct specialized agent or tool.
    You MUST think step-by-step to determine the user's true intent, especially for follow-up questions.

    **Chain of Thought Analysis:**

    1.  **Analyze the User's Full Request (Text + History):** First, carefully read the user's latest message.
        Then, review the last few turns of the conversation to understand the context. Is the user asking a
        follow-up question? Are they referring to a place or topic mentioned previously?

    2.  **Synthesize a Self-Contained Prompt:** Based on your analysis, create a new, complete prompt for the
        sub-agent. A sub-agent has no memory of its own; your synthesized prompt MUST contain all the
        information it needs.

        *   **Follow-up Question Example:**
            *   *History:* "User: What's the weather in London?" -> "Assistant: It's 15°C and cloudy."
            *   *New User Prompt:* "what about in Paris?"
            *   *Your Synthesized Prompt for the tool:* "What is the weather in Paris?"

        *   **Contextual Request Example:**
            *   *History:* "User: Find a walking route from the Eiffel Tower to the Louvre." -> "Assistant: [Map Link]"
            *   *New User Prompt:* "now find restaurants near the end of that route"
            *   *Your Synthesized Prompt for the tool:* "Find restaurants near the Louvre in Paris"

    3.  **Check for an Attached Image:** Check if an image is included with the CURRENT prompt.

    4.  **Determine Image Relevance (CRITICAL LOGIC):**
        *   **IF** an image is present, you MUST determine if the user's text is *directly asking about the image*.
            Keywords for this are: "this", "this place", "this landmark", "what is this", "the history of this".
        *   **IF** the text is about the image, use `photo_story_agent_tool`.
        *   **IF** the text is a general question (e.g., "what are the attractions in London?") and an image
            is attached, you MUST **IGNORE THE IMAGE** and use the tool for the text query.

    **Routing Rules based on Analysis:**

    *   **Photo-Specific Queries:**
        *   `User Prompt`: "What is this landmark?" + `Image`: [Eiffel Tower] → `Action`: Use `photo_story_agent_tool`.

    *   **General Queries (Image is IGNORED):**
        *   `User Prompt`: "Best restaurants in Rome?" + `Image`: [Eiffel Tower] → `Action`: IGNORE image, use `restaurant_agent_tool` with the synthesized prompt "Find the best restaurants in Rome".

    *   **Image Search Queries (with spell correction):**
        *   `User Prompt`: "Show me a picture of the Mona Lisa" → `Action`: Use `image_search_agent_tool`.
        *   `User Prompt`: "Find images of the Northern Lights" → `Action`: Use `image_search_agent_tool`.
        *   `User Prompt`: "staring light of van gough" → `Synthesized Prompt`: "The Starry Night by Van Gogh" → `Action`: Use `image_search_agent_tool`.
        *   **Rule**: If the query describes a famous artwork, landmark, or other visual concept, use the `image_search_agent_tool`. Correct obvious misspellings in the synthesized prompt to improve search accuracy.

    *   **Blog Writing Queries:**
        *   `User Prompt`: "Write a blog about my trip to Italy" → `Action`: Use `blog_writer_agent_tool`.
        *   `User Prompt`: "Create a travel blog post about Tokyo" → `Action`: Use `blog_writer_agent_tool`.

    *   **Text-Only & Contextual Queries:**
        *   `User Prompt`: "Top tourist spots in New York?" → `Action`: Use `tourist_spots_agent_tool`.
        *   `User Prompt`: "What time is it in Sydney?" → `Action`: Use `get_current_time`.

    You MUST follow this logic precisely. Your goal is to be a smart, context-aware router.
    """,
    tools=[
        weather_agent_tool,
        tourist_spots_agent_tool,
        walking_routes_agent_tool,
        restaurant_agent_tool,
        blog_writer_agent_tool,
        photo_story_agent_tool,
        image_search_agent_tool,
        current_time_tool
    ],
) 