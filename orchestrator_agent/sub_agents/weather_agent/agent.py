import requests
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Load environment variables
load_dotenv()

def get_city_weather(city: str) -> str:
    """Get real-time weather information for a specific city using OpenWeatherMap API."""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        return "Weather API key not configured. Please set OPENWEATHER_API_KEY in your .env file."
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 404:
            return f"City '{city}' not found. Please check the spelling or try a different city."
        
        if response.status_code != 200:
            return f"Error fetching weather data: {response.status_code}"
        
        weather_data = response.json()
        temp = weather_data["main"]["temp"]
        temp_f = (temp * 9/5) + 32
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        
        return (
            f"🌤️ Current Weather in {city}:\n"
            f"🌡️ Temperature: {temp:.1f}°C ({temp_f:.1f}°F)\n"
            f"☁️ Condition: {description.title()}\n"
            f"💧 Humidity: {humidity}%\n"
            f"💨 Wind Speed: {wind_speed} m/s\n\n"
            f"For the most up-to-date information, check Weather.com or your phone's weather app."
        )
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing weather data for '{city}'"

def get_current_time_and_location() -> str:
    """Get the current time and suggest weather for the user's current location."""
    try:
        # Get user's current timezone (this is a simplified approach)
        # In a real app, you'd get this from the user's device or IP
        current_time = datetime.now()
        
        # Common timezone mappings for major cities
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
        
        # For now, we'll use a default timezone (UTC) and suggest the user specify their location
        # In a real implementation, you'd detect the user's timezone
        utc_time = datetime.now(pytz.UTC)
        
        return (
            f"🕐 Current UTC Time: {utc_time.strftime('%I:%M %p, %A, %B %d, %Y')}\n\n"
            f"To get weather for your current location, please specify your city name.\n"
            f"Examples: 'What's the weather in Paris?' or 'Weather in New York'"
        )
        
    except Exception as e:
        return f"Error getting current time: {str(e)}"

def get_current_time(location: str) -> str:
    """Get the current time for a specific location."""
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
        return f"🕐 Current time in {location}: {current_time.strftime('%I:%M %p, %A, %B %d, %Y')} ({tz_name})"
    
    except Exception as e:
        return f"Error getting time for {location}: {str(e)}"

def get_weather_for_current_time() -> str:
    """Get weather information for the current time and suggest user's location."""
    current_info = get_current_time_and_location()
    return current_info

# Create tools without the name argument
weather_tool = FunctionTool(get_city_weather)
current_time_tool = FunctionTool(get_current_time)
current_weather_tool = FunctionTool(get_weather_for_current_time)

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="Provides weather information and current time for locations.",
    instruction="""
    You are a weather expert that provides weather information and current time.
    
    **How to respond:**
    - For weather questions: Use get_city_weather with the specified city
    - For current time: Use get_current_time with the specified location
    - For general weather queries: Use get_weather_for_current_time to show current time and ask for city
    
    **Examples:**
    - "Weather in Tokyo" → Get real-time weather for Tokyo
    - "Current time in London" → Get current time in London
    - "What's the weather?" → Show current time and ask for city
    
    Provide direct, helpful answers with weather information and travel recommendations.
    """,
    tools=[weather_tool, current_time_tool, current_weather_tool],
) 