from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema
from agents import chat, create_structured_prompt

accommodation_schemas = [
    ResponseSchema(name="name", description="The name of the accommodation"),
    ResponseSchema(name="location", description="The location of the accommodation"),
    ResponseSchema(name="price_per_night", description="The price per night"),
    ResponseSchema(name="total_price_for_week", description="The total price for a week"),
    ResponseSchema(name="features", description="List of features")
]

accommodation_template = """
Find current affordable hotel options for {numAdults} in {flightTo} for a stay from {flightDate} to {flightReturnDate}. Choose the top 3 options.
"""

accommodation_prompt, accommodation_parser = create_structured_prompt(accommodation_template, accommodation_schemas)
accommodation_chain = LLMChain(llm=chat, prompt=accommodation_prompt)
