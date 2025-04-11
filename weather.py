from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initializing FastMCP server
mcp = FastMCP("weather")

# Constants
# Update : Change the API from NWS to IMD
NWS_API_BASE = "https://api.weather.gov" 
USER_AGENT = "weather-app/1.0"


# Helper Functions
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Making request to the NWS API"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30)
            response.raise_for_status()
        except Exception:
            return None
        

def format_alert(feature: dict) -> str:
    """Formatting an alert feature into a readable str"""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
    """

# Tool Execution