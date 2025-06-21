from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from urllib.parse import quote_plus

def get_google_image_search_link(query: str) -> str:
    """
    Generates a Google Images search link for a given query.

    Args:
        query: The search term to find images for (e.g., "Mona Lisa", "Eiffel Tower at night").

    Returns:
        A URL that links directly to the Google Images search results for the query.
    """
    # URL encode the query to make it safe for a URL
    encoded_query = quote_plus(query)
    # Construct the Google Images search URL
    return f"https://www.google.com/search?tbm=isch&q={encoded_query}"

# Create a tool from the function
google_image_search_tool = FunctionTool(get_google_image_search_link)

# Create the image search agent
image_search_agent = Agent(
    name="image_search_agent",
    model="gemini-1.5-flash",
    description="An agent that finds Google Images search links for any visual query.",
    instruction="""
    You are a specialized image search assistant. Your sole purpose is to take a user's query
    and use the `get_google_image_search_link` tool to provide them with a direct link to the
    Google Images results.

    Do not add any extra commentary. Simply call the tool with the user's query and return the link.

    Example:
    User: "Show me pictures of the aurora borealis"
    You: Call `get_google_image_search_link` with the query "aurora borealis".
    """,
    tools=[google_image_search_tool],
) 