from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import urllib.parse

def generate_walking_route_map(start_location: str, end_location: str, waypoints: str = "") -> str:
    """
    Generate a Google Maps walking route link between locations.
    
    Args:
        start_location: Starting point (e.g., "Eiffel Tower, Paris")
        end_location: Ending point (e.g., "Louvre Museum, Paris")
        waypoints: Optional waypoints separated by | (e.g., "Notre Dame|Arc de Triomphe")
    
    Returns:
        Google Maps walking route URL
    """
    try:
        # Base Google Maps directions URL
        base_url = "https://www.google.com/maps/dir/"
        
        # Encode the locations
        start_encoded = urllib.parse.quote(start_location)
        end_encoded = urllib.parse.quote(end_location)
        
        # Build the URL
        url = f"{base_url}{start_encoded}/{end_encoded}"
        
        # Add waypoints if provided
        if waypoints:
            waypoints_encoded = urllib.parse.quote(waypoints.replace("|", "/"))
            url = f"{base_url}{start_encoded}/{waypoints_encoded}/{end_encoded}"
        
        # Add walking mode parameter
        url += "/data=!4m2!4m1!3e2"  # 3e2 specifies walking mode
        
        return f"Walking Route Map: {url}\n\nYou can click this link to open Google Maps with the walking directions from {start_location} to {end_location}."
    
    except Exception as e:
        return f"Error generating map link: {str(e)}"

def create_walking_plan_with_map(locations: str) -> str:
    """
    Create a comprehensive walking plan with map links for multiple tourist spots.
    If a city name is provided instead of specific locations, a default tour for that city is generated.
    
    Args:
        locations: Comma-separated list of spots (e.g., "Eiffel Tower, Louvre Museum") or a city name (e.g., "Paris").
    
    Returns:
        A step-by-step walking plan with Google Maps links.
    """
    try:
        # Predefined popular walking routes for major cities
        popular_routes = {
            "paris": "Eiffel Tower, Arc de Triomphe, Louvre Museum, Notre Dame Cathedral",
            "london": "Buckingham Palace, Big Ben, Tower of London, The British Museum",
            "rome": "Colosseum, Roman Forum, Trevi Fountain, Pantheon",
            "new york": "Times Square, Central Park, Statue of Liberty, Empire State Building"
        }

        # Check if the input is a known city for a default tour
        city_key = locations.lower().strip()
        if city_key in popular_routes:
            plan_intro = f"Here is a suggested walking tour for the top spots in {city_key.title()}:\n\n"
            locations = popular_routes[city_key]
        else:
            plan_intro = "Here is your custom walking route:\n\n"

        # Split locations and clean them
        spots = [spot.strip() for spot in locations.split(",") if spot.strip()]
        
        if len(spots) < 2:
            return "Please provide at least 2 locations or a major city name to create a walking route."
        
        plan = "🚶‍♂️ **Walking Route Plan**\n\n"
        plan += plan_intro
        
        # Create route between consecutive spots
        for i in range(len(spots) - 1):
            start = spots[i]
            end = spots[i + 1]
            
            plan += f"**Step {i + 1}: {start} → {end}**\n"
            
            # Generate map link for this segment
            map_link = generate_walking_route_map(start, end)
            plan += f"{map_link}\n"
            
            plan += f"Estimated walking time: 15-30 minutes (depending on distance)\n"
            plan += f"Distance: Varies (check map for exact distance)\n\n"
        
        # Create a complete route map if there are multiple waypoints
        if len(spots) > 2:
            waypoints = "|".join(spots[1:-1])  # All spots except first and last
            complete_route = generate_walking_route_map(spots[0], spots[-1], waypoints)
            plan += f"**Complete Route Map (All Stops):**\n{complete_route}\n\n"
        
        plan += "**Tips:**\n"
        plan += "• Use the map links to get real-time directions\n"
        plan += "• Check opening hours of attractions before visiting\n"
        plan += "• Consider rest stops and refreshments along the way\n"
        plan += "• Wear comfortable walking shoes\n"
        plan += "• Check weather conditions before starting your walk\n"
        
        return plan
    
    except Exception as e:
        return f"Error creating walking plan: {str(e)}"

# Create tools
walking_plan_tool = FunctionTool(
    create_walking_plan_with_map
)

walking_routes_agent = Agent(
    name="walking_routes_agent",
    model="gemini-1.5-flash",  # Ensure model is consistent
    description="Generates a step-by-step walking tour plan with Google Maps links for multiple tourist spots.",
    instruction="""
    You are a specialized agent that creates step-by-step walking tour plans.
    Your primary purpose is to use the `create_walking_plan_with_map` tool.

    When a user provides a list of two or more locations for a walking route, you MUST call the `create_walking_plan_with_map` tool with the locations.
    Do not answer conversationally; your only job is to format the locations and call the tool.
    """,
    tools=[walking_plan_tool],
)