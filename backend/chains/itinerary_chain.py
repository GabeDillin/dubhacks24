# chains/itinerary_chain.py

from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from agents import run_agent
from utils.logger import logger
from utils.llm import llm  # Centralized LLM instance
import json

# Define your response schemas
itinerary_schemas = [
    ResponseSchema(name="date", description="The day of the itinerary"),
    ResponseSchema(name="activities", description="List of activities with location"),
]

# Create a structured output parser
itinerary_parser = StructuredOutputParser.from_response_schemas(itinerary_schemas)
format_instructions = itinerary_parser.get_format_instructions()

# Define the prompt template
itinerary_template = f"""
Create an itinerary in the following JSON schema:

{format_instructions}

Itinerary Data:
{{
    "itineraryInfo": itineraryInfo
}}
"""

# Create the prompt
itinerary_prompt = ChatPromptTemplate.from_template(itinerary_template)

# Define a RunnableLambda for formatting the prompt
def format_itinerary_prompt(itinerary_info):
    return itinerary_prompt.format(itineraryInfo=itinerary_info)

runnable_format = RunnableLambda(format_itinerary_prompt)

# Define a RunnableLambda for invoking the agent
def invoke_agent(prompt):
    return run_agent(prompt)

runnable_invoke = RunnableLambda(invoke_agent)

# Define a RunnableLambda for parsing the response
def parse_itinerary_response(response):
    return itinerary_parser.parse(response)

runnable_parse = RunnableLambda(parse_itinerary_response)

# Compose the RunnableSequence: format_prompt -> agent.run -> parse_response
itinerary_sequence = RunnableSequence(
    [
        runnable_format,
        runnable_invoke,
        runnable_parse
    ]
)

def process_itinerary_info(itinerary_info):
    """
    Processes itinerary information and extracts structured itinerary data.

    Args:
        itinerary_info (dict): The raw itinerary information.

    Returns:
        dict: Structured itinerary information.
    """
    try:
        # Convert itinerary_info to JSON string
        itinerary_info_str = json.dumps(itinerary_info, indent=2)
        # Run the sequence with the itinerary information
        parsed = itinerary_sequence.invoke(itinerary_info_str)
        return parsed
    except Exception as e:
        logger.error(f"Error processing itinerary info: {e}")
        return {"error": str(e)}
