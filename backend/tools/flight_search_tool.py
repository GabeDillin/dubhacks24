# tools/flight_search_tool.py

from langchain.tools import Tool
from services.amadeus_service import search_flights
from utils.logger import logger

def flight_search_tool():
    """
    Defines the Flight Search tool for the agent.

    Returns:
        Tool: A LangChain Tool instance for searching flights.
    """
    def flight_search_func(params):
        try:
            return search_flights(**params)
        except Exception as e:
            logger.error(f"Flight search failed: {e}")
            return {"error": str(e)}

    return Tool(
        name="Flight Search",
        func=flight_search_func,
        description="Searches for flights based on origin, destination, departure date, return date, and number of adults."
    )
