# chains/final_chain.py

from langchain.prompts import ChatPromptTemplate
from langchain.runnables import RunnableSequence, RunnableLambda
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from agents import run_agent
from utils.logger import logger
from utils.llm import llm  # Centralized LLM instance
import json

# Define your response schemas
final_schemas = [
    ResponseSchema(name="flight_info", description="Detailed flight information"),
    ResponseSchema(name="accommodation_info", description="Detailed accommodation information"),
    ResponseSchema(name="itinerary_info", description="Detailed itinerary information"),
]

# Create a structured output parser
final_parser = StructuredOutputParser.from_response_schemas(final_schemas)
format_instructions = final_parser.get_format_instructions()

# Define the prompt template
final_template = f"""
Combine the following information into a comprehensive travel plan in the specified JSON schema:

{format_instructions}

Flight Information:
{{
    "flight_info": flight_info
}}

Accommodation Information:
{{
    "accommodation_info": accommodation_info
}}

Itinerary Information:
{{
    "itinerary_info": itinerary_info
}}
"""

# Create the prompt
final_prompt = ChatPromptTemplate.from_template(final_template)

# Define a RunnableLambda for formatting the final prompt
def format_final_prompt(flight_info, accommodation_info, itinerary_info):
    return final_prompt.format(
        flight_info=flight_info,
        accommodation_info=accommodation_info,
        itinerary_info=itinerary_info
    )

runnable_format = RunnableLambda(format_final_prompt)

# Define a RunnableLambda for invoking the agent
def invoke_agent(prompt):
    return run_agent(prompt)

runnable_invoke = RunnableLambda(invoke_agent)

# Define a RunnableLambda for parsing the response
def parse_final_response(response):
    return final_parser.parse(response)

runnable_parse = RunnableLambda(parse_final_response)

# Compose the RunnableSequence: format_prompt -> agent.run -> parse_response
final_sequence = RunnableSequence(
    [
        runnable_format,
        runnable_invoke,
        runnable_parse
    ]
)

def process_final_response(flight_info, accommodation_info, itinerary_info):
    """
    Combines flight, accommodation, and itinerary information into a final response.

    Args:
        flight_info (dict): Structured flight information.
        accommodation_info (dict): Structured accommodation information.
        itinerary_info (dict): Structured itinerary information.

    Returns:
        dict: Comprehensive travel plan.
    """
    try:
        # Prepare the input for the prompt
        prompt = final_sequence.invoke({
            "flight_info": flight_info,
            "accommodation_info": accommodation_info,
            "itinerary_info": itinerary_info
        })
        return prompt
    except Exception as e:
        logger.error(f"Error processing final response: {e}")
        return {"error": str(e)}
