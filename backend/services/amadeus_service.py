# services/amadeus_service.py

import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils.logger import logger

# Load environment variables from .env file
load_dotenv()

# Define the Amadeus credentials
CLIENT_ID = os.getenv("AMADEUS_API_KEY")        # Load API Key from environment
CLIENT_SECRET = os.getenv("AMADEUS_API_SECRET")  # Load API Secret from environment

# Token management
access_token = None
token_expiration = None

def get_access_token():
    """
    Request a new access token from the Amadeus API.

    Returns:
        str: Access token if successful.

    Raises:
        Exception: If the token request fails.
    """
    global access_token, token_expiration
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    # Request body for OAuth2 token
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    try:
        # Make the request
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info["access_token"]
        token_expiration = datetime.utcnow() + timedelta(seconds=token_info["expires_in"])
        logger.info("Access token acquired successfully.")
        return access_token
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get access token: {e}")

def ensure_access_token():
    """
    Ensure that a valid access token is available.

    Returns:
        str: Valid access token.

    Raises:
        Exception: If unable to acquire a valid access token.
    """
    global access_token, token_expiration
    if not access_token or (token_expiration and datetime.utcnow() >= token_expiration):
        logger.info("Fetching new access token...")
        return get_access_token()
    return access_token

def get_city_name_from_airport_code(airport_code):
    token = ensure_access_token()

    url = f"https://test.api.amadeus.com/v1/reference-data/locations?subType=AIRPORT&keyword={airport_code}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]['address']['cityName']
        else:
            raise Exception(f"No city found for airport code: {airport_code}")
    else:
        raise Exception(f"Failed to fetch city name for airport code: {airport_code}, Status code: {response.status_code}")

def search_flights(
    origin_location_code,
    destination_location_code,
    departure_date,
    adults,
    return_date=None,
    children=0,
    infants=0,
    travel_class=None,
    included_airline_codes=None,
    excluded_airline_codes=None,
    non_stop=False,
    currency_code="USD",
    max_price=None,
    max_offers=10
):
    """
    Search for flight offers using the Amadeus Flight Offers API.

    Args:
        origin_location_code (str): IATA code of the departure city/airport.
        destination_location_code (str): IATA code of the destination city/airport.
        departure_date (str): Departure date in 'YYYY-MM-DD' format.
        adults (int): Number of adult travelers.
        return_date (str, optional): Return date in 'YYYY-MM-DD' format.
        children (int, optional): Number of child travelers. Defaults to 0.
        infants (int, optional): Number of infant travelers. Defaults to 0.
        travel_class (str, optional): Travel class ('ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', 'FIRST'). Defaults to None.
        included_airline_codes (str, optional): Comma-separated list of airline IATA codes to include.
        excluded_airline_codes (str, optional): Comma-separated list of airline IATA codes to exclude.
        non_stop (bool, optional): If True, search for non-stop flights only. Defaults to False.
        currency_code (str, optional): Currency code for prices. Defaults to 'USD'.
        max_price (float, optional): Maximum price per traveler. Defaults to None.
        max_offers (int, optional): Maximum number of flight offers to return. Defaults to 10.

    Returns:
        dict: Raw JSON response from the Amadeus API.

    Raises:
        Exception: If the API request fails.
    """
    # Ensure a valid access token is available
    token = ensure_access_token()

    # Set up API request parameters
    params = {
        "originLocationCode": origin_location_code,
        "destinationLocationCode": destination_location_code,
        "departureDate": departure_date,
        "adults": adults,
        "max": max_offers,
        "nonStop": str(non_stop).lower(),
        "currencyCode": currency_code
    }

    if return_date:
        params["returnDate"] = return_date
    if children:
        params["children"] = children
    if infants:
        params["infants"] = infants
    if travel_class:
        params["travelClass"] = travel_class
    if included_airline_codes:
        params["includedAirlineCodes"] = included_airline_codes
    if excluded_airline_codes:
        params["excludedAirlineCodes"] = excluded_airline_codes
    if max_price:
        params["maxPrice"] = int(max_price)  # Assuming maxPrice should be an integer as per documentation

    base_url = "https://test.api.amadeus.com/v2"
    endpoint = "/shopping/flight-offers"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        # Make the API request
        response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data  # Return raw JSON
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors
        if response.status_code == 400:
            error_info = response.json().get("errors", [])
            if error_info:
                error = error_info[0]
                error_message = f"{error.get('title')}: {error.get('detail')}"
                raise Exception(f"API Error {error.get('status')}: {error_message}")
        elif response.status_code == 401:
            # Token might have expired; attempt to refresh once
            logger.info("Access token may have expired. Refreshing token and retrying...")
            global access_token
            access_token = None  # Reset token
            token = ensure_access_token()
            headers["Authorization"] = f"Bearer {token}"
            response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)
            try:
                response.raise_for_status()
                data = response.json()
                return data
            except requests.exceptions.RequestException as e:
                raise Exception(f"Failed after refreshing token: {e}")
        else:
            raise Exception(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions
        raise Exception(f"Request failed: {e}")
    except json.JSONDecodeError:
        # Handle JSON decoding errors
        raise Exception("Failed to parse JSON response from API.")
