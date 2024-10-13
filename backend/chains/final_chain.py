from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema
from agents import chat, create_structured_prompt

trip_schemas = [
    ResponseSchema(name="flights", description="List of flight options"),
    ResponseSchema(name="accommodation", description="List of accommodation options"),
    ResponseSchema(name="itinerary", description="Daily itinerary including activities, dining, and transportation")
]

final_template = """
Combine all three previous prompts to create a full trip plan for a {duration} day trip to {flightTo} from {flightDate} to {flightReturnDate}.
Each section should be its own json object, and the json entities should be the entities in the schema.
Flight options: {flight_info}
Accommodation options: {accommodation_info}
Itinerary options: {itinerary_info}
Only give me the json response, not the budget breakdown or any other text that would cause the response to be invalid for
json.loads(). Please include everything in a json format do not add comments at the end of your response. Also do not add any
comments to the json in this format :"// comment"
"""

final_prompt, final_parser = create_structured_prompt(final_template, trip_schemas)
final_chain = LLMChain(llm=chat, prompt=final_prompt)
