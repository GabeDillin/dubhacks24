from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from langchain.tools import BaseTool
from typing import Dict

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Define the Amadeus credentials
CLIENT_ID = os.getenv("AMADEUS_API_KEY")  # Load API Key from environment
CLIENT_SECRET = os.getenv("AMADEUS_API_SECRET")  # Load API Secret from environment

# Token management
access_token = None
token_expiration = None


def get_access_token():
    """Request a new access token from Amadeus API."""
    global access_token, token_expiration
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    
    # Request body for OAuth2 token
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    # Make the request
    response = requests.post(token_url, data=payload)
    token_info = response.json()
    
    if response.status_code == 200:
        access_token = token_info["access_token"]
        token_expiration = token_info["expires_in"]
        return access_token
    else:
        raise Exception(f"Failed to get access token: {response.text}")


class HotelSearchTool(BaseTool):
    name: str = "Hotel Search"
    description: str = "Search for hotel offers based on various parameters"

    def _run(self, query: str) -> str:
        params = self._parse_query(query)
        base_url = "https://test.api.amadeus.com/v2"
        endpoint = "/shopping/hotel-offers"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Make the API request
        response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)
        
        if response.status_code == 200:
            return self._format_response(response.json())
        else:
            return f"Error: {response.status_code}, {response.text}"

    def _parse_query(self, query: str) -> Dict[str, str]:
        params = {}
        if "hotel ids" in query.lower():
            params["hotelIds"] = query.split("hotel ids:")[-1].strip().split(",")
        if "check in" in query.lower():
            params["checkInDate"] = query.split("check in:")[-1].strip().split()[0]
        if "check out" in query.lower():
            params["checkOutDate"] = query.split("check out:")[-1].strip().split()[0]
        if "adults" in query.lower():
            params["adults"] = int(query.split("adults:")[-1].strip().split()[0])
        return params

    def _format_response(self, data: dict) -> str:
        offers = data.get("data", [])
        if not offers:
            return "No hotel offers found."
        
        formatted_offers = []
        for offer in offers[:5]:  # Limit to 5 offers
            hotel = offer.get("hotel", {})
            price = offer.get("offers", [{}])[0].get("price", {})
            formatted_offers.append(
                f"Hotel: {hotel.get('name')}, "
                f"Price: {price.get('total')} {price.get('currency')}"
            )
        
        return "\n".join(formatted_offers)