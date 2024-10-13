import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.chat_models import ChatPerplexity
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
from flightSearch import search_flights, get_city_name_from_airport_code

load_dotenv()

app = Flask(__name__)
CORS(app)

chat = ChatPerplexity(
    temperature=0,
    model="llama-3.1-sonar-small-128k-online",
    pplx_api_key=os.environ.get("PERPLEXITY_API_KEY")
)

def create_structured_prompt(template, response_schemas):
    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template + "\n{format_instructions}")
    return prompt, parser

flight_schemas = [
    ResponseSchema(name="airline", description="The name of the airline"),
    ResponseSchema(name="price", description="The price of the flight"),
    ResponseSchema(name="first_flight_depart", description="The departure time of the first flight"),
    ResponseSchema(name="first_flight_arrive", description="The arrival time of the first flight"),
    ResponseSchema(name="second_flight_depart", description="The departure time of the second flight"),
    ResponseSchema(name="second_flight_arive", description="The arrival time of the second flight"),
    ResponseSchema(name="first_flight_number", description="The flight number of the first flight"),
    ResponseSchema(name="second_flight_number", description="The flight number of the second flight"),
    ResponseSchema(name="emissions_data", description="Emissions data for the round trip"),
]

flight_prompt, flight_parser = create_structured_prompt(
    """From {flightOffers}, find round-trip flights from {flightFrom} to {flightTo} for a {duration} day trip from {flightDate} to {flightReturnDate}.
    The flight should be for {numAdults} adults. {flightOffers} is a json file that contains individual round-trip flights. Make sure all information matches with the specific round-trip.
    Prefer to look for three flights from different carriers/airlines if all three have full information ex: no "Unknown" or "missing". If not, find three round-trips that have full information.
    Do not include any round-trip twice.
    List flights with arrival time and departure time with date and hour, airline for both prices, as well as price for the round trip.
    Also display emissions information for each flight. The second flight information should be the return flight date and hour, not the first flight's information.
    """,
    flight_schemas
)

accommodation_schemas = [
    ResponseSchema(name="name", description="The name of the accommodation"),
    ResponseSchema(name="location", description="The location of the accommodation"),
    ResponseSchema(name="price_per_night", description="The price per night"),
    ResponseSchema(name="total_price_for_week", description="The total price for a week"),
    ResponseSchema(name="features", description="List of features")
]

accommodation_prompt, accommodation_parser = create_structured_prompt(
    "Find current affordable hotel options for {numAdults} in {flightTo} for a stay from {flightDate} to {flightReturnDate}. Choose the top 3 options.",
    accommodation_schemas
)

itinerary_schemas = [
    ResponseSchema(name="date", description="The day of the itinerary"),
    ResponseSchema(name="activities", description="List of activities with location"),
]

itinerary_prompt, itinerary_parser = create_structured_prompt(
    """Create an itinerary for {numAdults} for activities, dining, and transportation for a trip to {flightTo} from {flightDate} to {flightReturnDate}.
    The itinerary should be an array, and each date should be a sub-array with everything else in it. Each date should not be its own array, but should be a json object within the itinerary array.
    The activities on the first and last day when the guests are travelling should be less intense. The activities in the middle of the trip can be more intense.
    If the activities are intense, only include one activity per day. If they are less intense activities on days other than the first and last, include two activities per day.
    Include wellness tips and benefits for each activity, and should be an attribute under each activity. The first activity should be related to arrival and check in, but don't include any specific accommodation.
    The last activity should be departure, so returning to the airport and returning to {flightFrom}. Transportation should be included for each activity.
    Only give one option for dining per activity.
    """,
    itinerary_schemas
)

trip_schemas = [
    ResponseSchema(name="flights", description="List of flight options"),
    ResponseSchema(name="accommodation", description="List of accommodation options"),
    ResponseSchema(name="itinerary", description="Daily itinerary including activities, dining, and transportation")
]

final_prompt, final_parser = create_structured_prompt(
    """
    Combine all three previous prompts to create a full trip plan for a {duration} day trip to {flightTo} from {flightDate} to {flightReturnDate}.
    Each section should be its own json object, and the json entities should be the entities in the schema.
    Flight options: {flight_info}
    Accommodation options: {accommodation_info}
    Itinerary options: {itinerary_info}
    Each of these three sections should be a json array with each option being a json object.
    The itinerary should be a json array with each day being a json object. Each day should have a date and a list of activities.
    Only give me the json response, not the budget breakdown or any other text that would cause the response to be invalid for
    json.loads(). Please include everything in a json format do not add comments at the end of your response. Also do not add any
    comments to the json in this format :"// comment"
    """,
    trip_schemas
)

def run_chain_with_retry(chain, inputs, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chain.run(inputs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Attempt {attempt + 1} failed. Retrying...")

flight_chain = LLMChain(llm=chat, prompt=flight_prompt)
accommodation_chain = LLMChain(llm=chat, prompt=accommodation_prompt)
itinerary_chain = LLMChain(llm=chat, prompt=itinerary_prompt)
final_chain = LLMChain(llm=chat, prompt=final_prompt)

@app.route('/trip-info', methods=['POST'])
def trip_info():
    try:
        if request.is_json:
            data = request.get_json()
            flightFrom = data.get('flightFrom')
            flightTo = data.get('flightTo')
            flightDate = data.get('flightDate')
            flightReturnDate = data.get('flightReturnDate')
            budget = data.get('budget')
            numAdults = data.get('numAdults')

            flight_date_obj = datetime.strptime(flightDate, '%Y-%m-%d')
            flight_return_date_obj = datetime.strptime(flightReturnDate, '%Y-%m-%d')

            duration = (flight_return_date_obj - flight_date_obj).days

            cityFrom = get_city_name_from_airport_code(flightFrom)
            cityTo = get_city_name_from_airport_code(flightTo)

            flight_offers = []  # Initialize flight_offers to an empty list

            try:
                flight_search_params = {
                    "origin_location_code": flightFrom,
                    "destination_location_code": flightTo,
                    "departure_date": flightDate,
                    "return_date": flightReturnDate,
                    "adults": numAdults,
                    "max_offers": 5
                }

                flight_offers = search_flights(**flight_search_params)
                print("Raw Flight Offers JSON:")
                print(json.dumps(flight_offers, indent=2))
            except Exception as e:
                print(f"An error occurred during flight search: {e}")

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
                "flightTo": cityTo,
                "flightDate": flightDate,
                "flightReturnDate": flightReturnDate,
                "numAdults": numAdults,
                "format_instructions": accommodation_parser.get_format_instructions()
            })

            itinerary_info = run_chain_with_retry(itinerary_chain, {
                "flightTo": flightTo,
                "flightFrom": cityFrom,
                "flightDate": cityTo,
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

            try:
                parsed_response = final_parser.parse(final_response)
                return jsonify(parsed_response)
            except json.JSONDecodeError as e:
                return jsonify({"error": "Got invalid JSON object. Error: " + str(e), "raw_response": final_response}), 500
        else:
            return jsonify({"error": "Request content type must be application/json"}), 415
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)