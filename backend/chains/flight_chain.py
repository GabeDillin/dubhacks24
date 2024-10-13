# chains/flight_chain.py

from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from agents import run_agent
from utils.logger import logger
from utils.llm import llm  # Centralized LLM instance
import json

# Define your response schemas
flight_schemas = [
    ResponseSchema(name="airline", description="The name of the airline"),
    ResponseSchema(name="price", description="The price of the flight"),
    ResponseSchema(name="departure_time", description="The departure time of the flight"),
    ResponseSchema(name="arrival_time", description="The arrival time of the flight"),
    ResponseSchema(name="flight_number", description="The flight number"),
    ResponseSchema(name="emissions_data", description="Emissions data for the flight"),
]

# Create a structured output parser
flight_parser = StructuredOutputParser.from_response_schemas(flight_schemas)
format_instructions = flight_parser.get_format_instructions()

# Define the prompt template
flight_template = f"""
Extract the flight details in the following JSON schema:

{format_instructions}

Flight Offers:
{{
    "flightOffers": {{"data": flightOffers}}
}}
"""

# Create the prompt
flight_prompt = ChatPromptTemplate.from_template(flight_template)

# Define a RunnableLambda for processing the prompt
from langchain.runnables import RunnableLambda

def format_flight_prompt(flight_offers):
    return flight_prompt.format(flightOffers=flight_offers)

runnable_prompt = RunnableLambda(format_flight_prompt)

# Define a RunnableLambda for parsing the response
def parse_flight_response(response):
    return flight_parser.parse(response)

runnable_parse = RunnableLambda(parse_flight_response)

# Compose the sequence: format_prompt -> agent.run -> parse_response
flight_sequence = RunnableSequence(
    [
        runnable_prompt,
        RunnableLambda(run_agent),
        runnable_parse
    ]
)

def process_flight_info(flight_offers, flightFrom, flightTo, flightDate, flightReturnDate):
    """
    Processes flight offers and extracts structured flight information.

    Args:
        flight_offers (dict): The raw flight offers data.
        flightFrom (str): Origin airport code.
        flightTo (str): Destination airport code.
        flightDate (str): Departure date.
        flightReturnDate (str): Return date.

    Returns:
        dict: Structured flight information.
    """
    try:
        # Prepare the input for the prompt
        flight_offers_str = json.dumps(flight_offers, indent=2)
        # Run the sequence with the flight offers
        parsed = flight_sequence.invoke(flight_offers_str)
        return parsed
    except Exception as e:
        logger.error(f"Error processing flight info: {e}")
        return {"error": str(e)}
