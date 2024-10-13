# routes/trip_info_route.py

from flask import Blueprint, jsonify
from utils import parse_request_data, logger
from agents import run_chain_with_retry
from chains import (
    flight_chain, flight_parser,
    accommodation_chain, accommodation_parser,
    itinerary_chain, itinerary_parser,
    final_chain, final_parser
)
from tools.flight_search import search_flights, get_city_name_from_airport_code

trip_info_route = Blueprint('trip_info_route', __name__)

@trip_info_route.route('/trip-info', methods=['POST'])
def trip_info():
    try:
        data = parse_request_data()
        flightFrom = data['flightFrom']
        flightTo = data['flightTo']
        flightDate = data['flightDate']
        flightReturnDate = data['flightReturnDate']
        budget = data['budget']
        numAdults = data['numAdults']
        duration = data['duration']

        cityFrom = get_city_name_from_airport_code(flightFrom)
        cityTo = get_city_name_from_airport_code(flightTo)

        flight_search_params = {
            "origin_location_code": flightFrom,
            "destination_location_code": flightTo,
            "departure_date": flightDate,
            "return_date": flightReturnDate,
            "adults": numAdults,
            "max_offers": 5
        }
        flight_offers = search_flights(**flight_search_params)
        logger.info("Flight offers retrieved successfully.")

        flight_info = run_chain_with_retry(flight_chain, {
            "flightFrom": flightFrom,
            "flightTo": flightTo,
            "flightDate": flightDate,
            "flightReturnDate": flightReturnDate,
            "flightOffers": flight_offers,
            "duration": duration,
            "numAdults": numAdults,
            "format_instructions": flight_parser.get_format_instructions()
        })

        accommodation_info = run_chain_with_retry(accommodation_chain, {
            "flightTo": flightTo,
            "flightDate": flightDate,
            "flightReturnDate": flightReturnDate,
            "numAdults": numAdults,
            "format_instructions": accommodation_parser.get_format_instructions()
        })

        itinerary_info = run_chain_with_retry(itinerary_chain, {
            "flightTo": flightTo,
            "flightFrom": flightFrom,
            "flightDate": flightDate,
            "flightReturnDate": flightReturnDate,
            "duration": duration,
            "budget": budget,
            "numAdults": numAdults,
            "format_instructions": itinerary_parser.get_format_instructions()
        })

        final_response = run_chain_with_retry(final_chain, {
            "flight_info": flight_info,
            "accommodation_info": accommodation_info,
            "itinerary_info": itinerary_info,
            "flightTo": flightTo,
            "flightFrom": flightFrom,
            "flightDate": flightDate,
            "flightReturnDate": flightReturnDate,
            "duration": duration,
            "budget": budget,
            "format_instructions": final_parser.get_format_instructions()
        })

        parsed_response = final_parser.parse(final_response)
        return jsonify(parsed_response), 200
    except Exception as e:
        logger.exception("An error occurred in trip_info endpoint.")
        return jsonify({"error": str(e)}), 500
