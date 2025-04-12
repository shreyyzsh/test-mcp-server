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
@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Getting weather alerts for a US State.
    
    Args:
        state: two-letter us state code (e.g CA, NY)
    """
    
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "No active alerts for this state."
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n--\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Getting weather forecast for a location.
    
    Args:
        latitude: latitude of the location
        longitude: longitude of the location
    """
    
    # Getting the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch forecast data for this location"
    
    # Doubt : what's happening here?
    # Getting the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    
    if not forecast_data:
        return "unable to fetch detailed forecast"
   
    # Doubt : what's happening here? 
    # Formatting the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]: # Only showing next 5 periods
        forecast = f"""
            {period['name']}:
            Temperature: {period['temperature']}°{period['temperatureUnit']}
            Wind: {period['windSpeed']} {period['windDirection']}
            Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)
    
    return "\n---\n".join(forecasts)

# Running the server
if __name__ == "__main__":
    mcp.run(transport='stdio')