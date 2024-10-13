# tools/flight_search.py

from services.amadeus_service import (
    search_flights as amadeus_search_flights,
    get_city_name_from_airport_code as amadeus_get_city_name_from_airport_code
)
from utils.logger import logger

def get_city_name_from_airport_code(airport_code):
    try:
        return amadeus_get_city_name_from_airport_code(airport_code)
    except Exception as e:
        logger.exception(f"Error getting city name for airport code {airport_code}: {e}")
        raise e

def search_flights(**kwargs):
    try:
        print("searching flights")
        return amadeus_search_flights(**kwargs)
    except Exception as e:
        logger.exception(f"Error searching flights: {e}")
        raise e
