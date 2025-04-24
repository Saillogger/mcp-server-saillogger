from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("saillogger")

# Constants
API_BASE = "https://saillogger.com/ais/api"
USER_AGENT = "Saillogger MCP Server"

async def make_ais_request(url: str) -> dict[str, Any] | None:
    """ Make a request to Saillogger """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_vessel(vessel: dict) -> str:
    """Format the details as readable string."""
    AIS_SHIP_TYPES = {
        30: "Fishing Vessel",
        31: "Towing Vessel",
        32: "Towing vessel length > 200m",
        33: "Dredging/Underwater Operations",
        34: "Diving Operations",
        35: "Military Operations",
        36: "Sailing Vessel",
        37: "Pleasure Craft",
        40: "High Speed Craft",
        50: "Pilot Vessel",
        51: "Search and Rescue",
        52: "Tug",
        53: "Port Tender",
        54: "Anti-Pollution Equipment",
        55: "Law Enforcement",
        58: "Medical Transport",
        59: "Special Craft",
        60: "Passenger Ship",
        70: "Cargo Ship",
        71: "Tanker",
        72: "Hazardous Cargo Ship",
        80: "Commercial Ship"
    }
    return f"""
Name: {vessel.get('name', 'Unknown')}
Type: {AIS_SHIP_TYPES.get(vessel.get('type', '0'), 'Unknown')}
MMSI: {vessel.get('mmsi', 'Unknown')}
Coordinates: {vessel.get('latitude', 'Unknown')}, {vessel.get('longitude', 'Unknown')}
Course Over Ground: {vessel.get('course_over_ground', 'Unknown')}
Speed: {vessel.get('speed_over_ground', 'Unknown')}
"""

@mcp.tool()
async def get_ais_targets(latitude: float, longitude: float, radius: float, start: int = 1, count: int = 25) -> str:
    """Get AIS targets within a radius of a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        radius: Radius in nautical miles (maximum is 10)
    """
    url = f"{API_BASE}/vessels/?format=json&latitude={latitude}&longitude={longitude}&radius_nm={radius}"
    ais_data = await make_ais_request(url)

    if not ais_data:
        return "Unable to retrieve AIS targets for this position."

    if ais_data:
        response = f"Found {len(ais_data)} vessels in the area:\n"
        response += f"Latitude: {latitude}, Longitude: {longitude}, Radius: {radius} nautical miles\n"
        response += f"Vessels:\n"
        counter = 1
        for vessel in ais_data[start - 1:]:
            # Format each vessel's details
            response += f"Vessel {counter}:\n"
            counter += 1
            # Add vessel details to the response
            response += format_vessel(vessel)
            if counter > count:
                response += f"\nI will stop providing details here."
                response += f"But you can ask for more, just start the page from {counter + count - 1}.\n"
                break

        return response
    else:
        return "No vessels found in the area."

def main():
    """Entry point for the application."""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main() 
