from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import requests
import json
import re
from urllib.parse import quote_plus

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

get_attraction_image_tool = FunctionTool(get_attraction_image)

tourist_spots_agent = Agent(
    name="tourist_spots_agent",
    model="gemini-2.0-flash",
    description="Finds top tourist spots for a given location and provides image links via tool calls.",
    instruction="""
    You are a travel expert that recommends top tourist spots and attractions.
    
    When asked about tourist spots, provide comprehensive recommendations including:
    - Must-see landmarks and attractions
    - Historical sites and cultural venues
    - Popular neighborhoods and districts
    - Hidden gems and local favorites
    - Best times to visit each attraction
    - Practical tips for visiting
    
    For each major attraction or landmark you mention, CALL the get_attraction_image tool with the attraction name and location, and include the returned image URL in your response as a thumbnail.
    
    Example format:
    **Eiffel Tower:**
    ![Eiffel Tower](<image_url>)
    The iconic symbol of Paris, standing 324 meters tall...
    
    **Louvre Museum:**
    ![Louvre Museum](<image_url>)
    Home to world-renowned masterpieces like the Mona Lisa...
    
    Provide direct, helpful recommendations for the requested location. Always include image thumbnails for at least 5-8 major attractions.
    """,
    tools=[get_attraction_image_tool],
)