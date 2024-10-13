import os
import json
from flask import Flask, request, jsonify
from langchain_community.chat_models import ChatPerplexity
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

chat = ChatPerplexity(
    temperature=0.4,
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
    ResponseSchema(name="link", description="The link to the flight"),
    ResponseSchema(name="first_flight_depart", description="The departure time of the first flight"),
    ResponseSchema(name="first_flight_arrive", description="The arrival time of the first flight"),
    ResponseSchema(name="second_flight_depart", description="The departure time of the second flight"),
    ResponseSchema(name="second_flight_arive", description="The arrival time of the second flight"),
    ResponseSchema(name="emissions_data", description="Emissions data for the round trip")
    
]

flight_prompt, flight_parser = create_structured_prompt(
    """Find current round-trip flights from {flightFrom} to {flightTo} for a 1-long trip from {flightDate} to {flightReturnDate}. 
    List top 3 flights with arrival time and departure time with date and hour, airline for both prices, as well as price for the round trip.
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
    "Find current affordable hotel options in {flightTo} for a stay from {flightDate} to {flightReturnDate}. Choose the top 3 options.",
    accommodation_schemas
)

itinerary_schemas = [
    ResponseSchema(name="date", description="The day of the itinerary"),
    ResponseSchema(name="activities", description="List of activities with location"),
    ResponseSchema(name="travel", description="Forms of transportation for each activity"),
    ResponseSchema(name="dining", description="List of dining options with location, price, and cuisine"),
    ResponseSchema(name="wellness", description="List of wellness tips/benefits for each activity")
]

itinerary_prompt, itinerary_parser = create_structured_prompt(
    """Create an itinerary for activities, dining, and transportation for a {duration} trip to {flightTo} from {flightDate} to {flightReturnDate}.
    Include wellness tips and benefits for each activity. The first activity should be related to arrival and check in, but don't include any specific accommodation.
    The last activity should be departure, so returning to the airport and returning to {flightFrom}. Transportation should be included for each activity.
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
    Combine all three previous prompts to create a full trip plan for a {duration} trip to {flightTo} from {flightDate} to {flightReturnDate}.
    Each section should be its own json object, and the json entities should be the entities in the schema.
    Flight options: {flight_info}
    Accommodation options: {accommodation_info}
    Itinerary options: {itinerary_info}
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
            duration = data.get('duration')
            budget = data.get('budget')

            flight_info = run_chain_with_retry(flight_chain, {
                "flightFrom": flightFrom,
                "flightTo": flightTo,
                "flightDate": flightDate,
                "flightReturnDate": flightReturnDate,
                "format_instructions": flight_parser.get_format_instructions()
            })
            
            accommodation_info = run_chain_with_retry(accommodation_chain, {
                "flightTo": flightTo,
                "flightDate": flightDate,
                "flightReturnDate": flightReturnDate,
                "format_instructions": accommodation_parser.get_format_instructions()
            })

            itinerary_info = run_chain_with_retry(itinerary_chain, {
                "flightTo": flightTo,
                "flightFrom": flightFrom,
                "flightDate": flightDate,
                "flightReturnDate": flightReturnDate,
                "duration": duration,
                "budget": budget,
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

            # Log the raw response for debugging
            print("Raw response:", final_response)

            # Attempt to parse the JSON response
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