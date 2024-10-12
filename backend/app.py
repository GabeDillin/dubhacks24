import os
import json
from langchain_community.chat_models import ChatPerplexity
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

chat = ChatPerplexity(
    temperature=0.7,
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
    ResponseSchema(name="flight_number", description="The flight number"),
    ResponseSchema(name="departure_time", description="The departure time"),
    ResponseSchema(name="arrival_time", description="The arrival time")
]

flight_prompt, flight_parser = create_structured_prompt(
    "Find current round-trip flights from LAX to Seattle for a week-long trip from 10/20/2024 to 10/27/2024. List top 3 options.",
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
    "Find current affordable hotel or Airbnb options in Seattle for a stay from 10/20/2024 to 10/27/2024. List top 3 options.",
    accommodation_schemas
)

trip_schemas = [
    ResponseSchema(name="flights", description="List of flight options"),
    ResponseSchema(name="accommodation", description="List of accommodation options"),
    ResponseSchema(name="itinerary", description="Daily itinerary including activities, dining, and transportation")
]

final_prompt, final_parser = create_structured_prompt(
    """
    Based on the provided flight and accommodation information, create a 1-week trip to Seattle from 10/20/2024 to 10/27/2024 with a total budget of $2000 USD.
    Include flights, accommodation, and a comprehensive daily itinerary with activities, dining, and transportation.
    
    Flight options: {flight_info}
    Accommodation options: {accommodation_info}
    Only give me the json response, not the budget breakdown or any other text that would cause the response to be invalid for
    json.loads().
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
final_chain = LLMChain(llm=chat, prompt=final_prompt)

flight_info = run_chain_with_retry(flight_chain, {"format_instructions": flight_parser.get_format_instructions()})
accommodation_info = run_chain_with_retry(accommodation_chain, {"format_instructions": accommodation_parser.get_format_instructions()})

final_response = run_chain_with_retry(final_chain, {
    "flight_info": flight_info,
    "accommodation_info": accommodation_info,
    "format_instructions": final_parser.get_format_instructions()
})

try:
    parsed_response = final_parser.parse(final_response)
    print(json.dumps(parsed_response, indent=2))
except Exception as e:
    print("Error parsing response:", e)
    print("Raw response:")
    print(final_response)