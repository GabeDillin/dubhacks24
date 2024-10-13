# services/hotel_service.py

import requests
from config import Config
from utils.logger import logger

def search_hotels(
    location,
    check_in_date,
    check_out_date,
    adults,
    max_results=5
):
    """
    Search for hotels using the Google Places API.

    Args:
        location (str): Location to search for hotels.
        check_in_date (str): Check-in date in 'YYYY-MM-DD' format.
        check_out_date (str): Check-out date in 'YYYY-MM-DD' format.
        adults (int): Number of adult travelers.
        max_results (int, optional): Maximum number of results to return. Defaults to 5.

    Returns:
        dict: List of hotels with relevant details.

    Raises:
        Exception: If the API request fails.
    """
    try:
        # Geocoding to get latitude and longitude from location
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geocode_params = {
            "address": location,
            "key": Config.GOOGLE_API_KEY
        }
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if geocode_data['status'] != 'OK':
            logger.error(f"Geocoding failed: {geocode_data['status']}")
            raise Exception(f"Geocoding failed: {geocode_data['status']}")

        latlng = geocode_data['results'][0]['geometry']['location']
        latitude = latlng['lat']
        longitude = latlng['lng']

        # Searching for hotels using Places API Nearby Search
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places_params = {
            "location": f"{latitude},{longitude}",
            "radius": 15000,  # in meters
            "type": "lodging",
            "key": Config.GOOGLE_API_KEY
        }
        places_response = requests.get(places_url, params=places_params)
        places_response.raise_for_status()
        places_data = places_response.json()

        if places_data['status'] != 'OK':
            logger.error(f"Places API failed: {places_data['status']}")
            raise Exception(f"Places API failed: {places_data['status']}")

        # Limit the results to max_results
        hotels = places_data['results'][:max_results]

        # Extract necessary details
        hotel_list = []
        for hotel in hotels:
            hotel_info = {
                "name": hotel.get("name"),
                "address": hotel.get("vicinity"),
                "rating": hotel.get("rating"),
                "user_ratings_total": hotel.get("user_ratings_total"),
                "price_level": hotel.get("price_level"),
                "place_id": hotel.get("place_id")
            }
            hotel_list.append(hotel_info)

        return {"hotels": hotel_list}

    except requests.exceptions.RequestException as e:
        logger.error(f"Google Places API request failed: {e}")
        raise Exception(f"Google Places API request failed: {e}")
    except Exception as e:
        logger.error(f"Error in search_hotels: {e}")
        raise e
