# routes/trip_info_route.py

from flask import Blueprint, jsonify
from utils import parse_request_data, logger
from chains import (
    flight_sequence, flight_parser, process_flight_info,
    accommodation_sequence, accommodation_parser, process_accommodation_info,
    itinerary_sequence, itinerary_parser, process_itinerary_info,
    final_sequence, final_parser, process_final_response
)
from agents import run_agent
import json
from datetime import datetime

trip_info_route = Blueprint('trip_info_route', __name__)

@trip_info_route.route('/trip-info', methods=['POST'])
def trip_info():
    try:
        # Parse the incoming request data
        data = parse_request_data()
        flightFrom = data['flightFrom']
        flightTo = data['flightTo']
        flightDate = data['flightDate']
        flightReturnDate = data['flightReturnDate']
        budget = data['budget']
        numAdults = data['numAdults']
        
        # Calculate duration based on flight dates
        flight_date_obj = datetime.strptime(flightDate, "%Y-%m-%d")
        return_date_obj = datetime.strptime(flightReturnDate, "%Y-%m-%d")
        duration = (return_date_obj - flight_date_obj).days

        # Prepare parameters for flight search
        flight_search_params = {
            "origin_location_code": flightFrom,
            "destination_location_code": flightTo,
            "departure_date": flightDate,
            "return_date": flightReturnDate,
            "adults": numAdults,
            "max_offers": 5
        }

        # Run the flight search tool via agent
        flight_offers = run_agent(flight_search_params)
        logger.info("Flight offers retrieved successfully.")

        # Process flight offers to extract structured flight information
        flight_info = process_flight_info(
            flight_offers=flight_offers,
            flightFrom=flightFrom,
            flightTo=flightTo,
            flightDate=flightDate,
            flightReturnDate=flightReturnDate
        )
        logger.info("Flight information processed successfully.")

        # Prepare parameters for accommodation search
        accommodation_search_params = {
            "location": flightTo,
            "check_in_date": flightDate,
            "check_out_date": flightReturnDate,
            "adults": numAdults,
            "max_results": 5
        }

        # Run the accommodation search tool via agent
        accommodation_data = run_agent(accommodation_search_params)
        logger.info("Accommodation data retrieved successfully.")

        # Process accommodation data to extract structured accommodation information
        accommodation_info = process_accommodation_info(
            accommodation_data=accommodation_data,
            location=flightTo,
            check_in_date=flightDate,
            check_out_date=flightReturnDate,
            numAdults=numAdults
        )
        logger.info("Accommodation information processed successfully.")

        # Prepare itinerary information
        itinerary_info = {
            "date": flightDate,
            "activities": [
                {"activity": "Departure from SEA", "location": flightFrom},
                {"activity": "Arrival at LAX", "location": flightTo},
                {"activity": "Check into hotel", "location": accommodation_info.get("name")},
                {"activity": "Attend meetings/conferences", "location": flightTo},
                {"activity": "Dinner at a local restaurant", "location": flightTo},
                {"activity": "Departure from LAX", "location": flightTo},
                {"activity": "Arrival at SEA", "location": flightFrom}
            ]
        }

        # Convert itinerary_info to JSON string for processing
        itinerary_info_str = json.dumps(itinerary_info, indent=2)

        # Process itinerary information to extract structured itinerary data
        structured_itinerary_info = process_itinerary_info(itinerary_info_str)
        logger.info("Itinerary information processed successfully.")

        # Combine all information into the final response
        final_response = process_final_response(
            flight_info=flight_info,
            accommodation_info=accommodation_info,
            itinerary_info=structured_itinerary_info
        )
        logger.info("Final response generated successfully.")

        # Since final_response is a dict, return it directly
        return jsonify(final_response), 200

    except Exception as e:
        logger.exception("An error occurred in trip_info endpoint.")
        return jsonify({"error": str(e)}), 500
