# Claude-NWS Protocol Bridge

A Model Context Protocol (MCP) server that integrates the US National Weather Service API with Claude Desktop, providing real-time weather data and forecasts directly within your Claude conversations.

## Features

- 🌤️ Real-time weather conditions and forecasts
- 🗺️ Location-based weather queries using coordinates or place names
- ⚡ Seamless integration with Claude Desktop via MCP
- 🔄 Live data from the official US National Weather Service API
- 📊 Detailed weather metrics including temperature, humidity, wind, and precipitation

## Prerequisites

- Claude Desktop App
- Python (v3.12 or higher)
- uv package manager
- Internet connection for API access

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/claude-nws-protocol-bridge.git
   cd claude-nws-protocol-bridge
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Configure the MCP server in your Claude Desktop settings:
   ```json
   {
    "mcpServers": {
      "nws-weather": {
        "command": "uv",
        "args": ["run", "python", "weather.py"]
      }
    }
   }
   ```

## Usage

Once configured, you can ask Claude weather-related questions such as:

- "What's the current weather in San Francisco?"
- "Give me a 7-day forecast for New York City"
- "What's the temperature and humidity right now?"
- "Is it going to rain today in Seattle?"

## API Reference

The bridge provides the following MCP tools:

### `get-current-weather`
Retrieves current weather conditions for a specified location.

**Parameters:**
- `location` (string): City name, coordinates, or ZIP code

### `get-weather-forecast`
Gets weather forecast data for a specified location.

**Parameters:**
- `location` (string): City name, coordinates, or ZIP code
- `days` (number, optional): Number of forecast days (default: 7)

