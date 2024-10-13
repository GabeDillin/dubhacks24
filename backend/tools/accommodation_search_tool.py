# tools/accommodation_search_tool.py

from langchain.tools import Tool
from services.hotel_service import search_hotels
from utils.logger import logger

def accommodation_search_tool():
    """
    Defines the Accommodation Search tool for the agent.

    Returns:
        Tool: A LangChain Tool instance for searching accommodations.
    """
    def accommodation_search_func(params):
        try:
            location = params.get("location")
            check_in_date = params.get("check_in_date")
            check_out_date = params.get("check_out_date")
            adults = params.get("adults", 1)
            max_results = params.get("max_results", 5)
            return search_hotels(
                location=location,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                adults=adults,
                max_results=max_results
            )
        except Exception as e:
            logger.error(f"Accommodation search failed: {e}")
            return {"error": str(e)}

    return Tool(
        name="Accommodation Search",
        func=accommodation_search_func,
        description="Searches for accommodations based on location, check-in date, check-out date, and number of adults."
    )
