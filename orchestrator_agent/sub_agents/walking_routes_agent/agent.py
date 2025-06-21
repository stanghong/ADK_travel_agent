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
    
    Args:
        locations: Comma-separated list of tourist spots (e.g., "Eiffel Tower, Louvre Museum, Notre Dame, Arc de Triomphe")
    
    Returns:
        Walking plan with map links
    """
    try:
        # Split locations and clean them
        spots = [spot.strip() for spot in locations.split(",") if spot.strip()]
        
        if len(spots) < 2:
            return "Please provide at least 2 locations to create a walking route."
        
        plan = "🚶‍♂️ **Walking Route Plan**\n\n"
        
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
walking_route_map_tool = FunctionTool(generate_walking_route_map)
walking_plan_tool = FunctionTool(create_walking_plan_with_map)

walking_routes_agent = Agent(
    name="walking_routes_agent",
    model="gemini-2.0-flash",
    description="Maps out walking routes for tourist spots with Google Maps links.",
    instruction="""
    You are a walking tour expert that creates detailed walking routes for tourists.
    
    When asked about walking routes, provide comprehensive route planning including:
    - Step-by-step directions between attractions
    - Google Maps links for each route segment
    - Estimated walking times and distances
    - Points of interest along the way
    - Rest stops and refreshment options
    - Safety tips and best practices
    - Alternative routes for different preferences
    
    Use the available tools to generate map links for walking routes.
    When users ask for map links based on a walking plan, use the tools to create
    Google Maps directions that they can follow.
    
    Provide direct, helpful walking route recommendations with practical navigation assistance.
    """,
    tools=[walking_route_map_tool, walking_plan_tool],
)