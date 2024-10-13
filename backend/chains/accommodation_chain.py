# chains/accommodation_chain.py

from langchain.prompts import ChatPromptTemplate
from langchain.runnables import RunnableSequence, RunnableLambda
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from agents import run_agent
from utils.logger import logger
from utils.llm import llm  # Centralized LLM instance
import json

# Define your response schemas
accommodation_schemas = [
    ResponseSchema(name="name", description="The name of the accommodation"),
    ResponseSchema(name="address", description="The address of the accommodation"),
    ResponseSchema(name="rating", description="The rating of the accommodation"),
    ResponseSchema(name="user_ratings_total", description="Total number of user ratings"),
    ResponseSchema(name="price_level", description="Price level of the accommodation"),
    ResponseSchema(name="place_id", description="Place ID of the accommodation"),
]

# Create a structured output parser
accommodation_parser = StructuredOutputParser.from_response_schemas(accommodation_schemas)
format_instructions = accommodation_parser.get_format_instructions()

# Define the prompt template
accommodation_template = f"""
Extract the accommodation details in the following JSON schema:

{format_instructions}

Accommodation Data:
{{
    "hotels": hotels
}}
"""

# Create the prompt
accommodation_prompt = ChatPromptTemplate.from_template(accommodation_template)


# Define a RunnableLambda for processing the prompt
def format_accommodation_prompt(accommodation_data):
    return accommodation_prompt.format(hotels=accommodation_data)

runnable_prompt = RunnableLambda(format_accommodation_prompt)

# Define a RunnableLambda for parsing the response
def parse_accommodation_response(response):
    return accommodation_parser.parse(response)

runnable_parse = RunnableLambda(parse_accommodation_response)

# Compose the sequence: format_prompt -> agent.run -> parse_response
accommodation_sequence = RunnableSequence(
    [
        runnable_prompt,
        RunnableLambda(run_agent),
        runnable_parse
    ]
)

def process_accommodation_info(accommodation_data, location, check_in_date, check_out_date, numAdults):
    """
    Processes accommodation data and extracts structured accommodation information.

    Args:
        accommodation_data (dict): The raw accommodation data.
        location (str): Location of the accommodation.
        check_in_date (str): Check-in date.
        check_out_date (str): Check-out date.
        numAdults (int): Number of adult travelers.

    Returns:
        dict: Structured accommodation information.
    """
    try:
        # Prepare the input for the prompt
        accommodation_info_str = json.dumps(accommodation_data, indent=2)
        prompt = accommodation_prompt.format(
            hotels=accommodation_info_str
        )
        # Run the agent with the prompt
        response = run_agent(prompt)
        # Parse the response using the structured parser
        parsed = accommodation_parser.parse(response)
        return parsed
    except Exception as e:
        logger.error(f"Error processing accommodation info: {e}")
        return {"error": str(e)}
