from google.adk.agents import Agent
from .sub_agents.weather_agent.agent import weather_agent
from .sub_agents.tourist_spots_agent.agent import tourist_spots_agent
from .sub_agents.blog_writer_agent.agent import blog_writer_agent
from .sub_agents.walking_routes_agent.agent import walking_routes_agent
from .sub_agents.restaurant_recommendation_agent.agent import restaurant_recommendation_agent
from .sub_agents.photo_story_agent.agent import photo_story_agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
from datetime import datetime
import pytz

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

current_time_tool = FunctionTool(get_current_time)

root_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.0-flash",
    description="Orchestrates travel queries, delegating to sub-agents for weather, tourist spots, blog writing, routes, restaurants, and photo stories.",
    instruction="""
    You are a travel assistant that maintains conversation context and remembers previous interactions within the same session.
    
    When a user asks a question, decide which sub-agent(s) to use:
    - Weather Agent: for weather info and current time
    - Tourist Spots Agent: for top places to visit
    - Blog Writer Agent: to generate travel blogs
    - Walking Routes Agent: to map out walking routes with Google Maps links
    - Restaurant Recommendation Agent: for food suggestions
    - Photo Story Agent: for stories based on photos
    
    You can also handle current time queries directly using the get_current_time tool.
    When asked about current time in a location, use the tool to provide accurate time information.
    
    The Walking Routes Agent can now generate Google Maps links for walking directions between tourist spots.
    When users ask for map links based on a walking plan, the agent will provide clickable Google Maps URLs.
    
    **IMPORTANT: Conversation Memory**
    - Always reference previous conversations and context from the same session
    - If a user refers to something mentioned earlier (like "the places we discussed" or "that walking route"), use that context
    - Build upon previous recommendations and avoid repeating information unless asked
    - If a user asks follow-up questions, reference the specific details from earlier in the conversation
    - Maintain continuity in recommendations and suggestions across the session
    
    **Context Awareness Examples:**
    - If user previously asked about Paris attractions, and now asks "give me a walking route between those places", use the previously mentioned locations
    - If user asked about weather in Tokyo and now asks "what should I pack", reference the weather conditions mentioned earlier
    - If user discussed restaurant preferences earlier, consider those when making new recommendations
    
    Combine results and present a helpful answer that builds upon the conversation history.
    """,
    sub_agents=[
        weather_agent,
        tourist_spots_agent,
        blog_writer_agent,
        walking_routes_agent,
        restaurant_recommendation_agent,
        photo_story_agent,
    ],
    tools=[current_time_tool],
) 