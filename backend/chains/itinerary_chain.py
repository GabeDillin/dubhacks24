from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema
from agents import chat, create_structured_prompt

itinerary_schemas = [
    ResponseSchema(name="date", description="The day of the itinerary"),
    ResponseSchema(name="activities", description="List of activities with location")
]

itinerary_template = """
Create an itinerary for {numAdults} for activities, dining, and transportation for a trip to {flightTo} from {flightDate} to {flightReturnDate}.
The activities on the first and last day when the guests are travelling should be less intense. The activities in the middle of the trip can be more intense.
If the activities are intense, only include one activity per day. If they are less intense activities on days other than the first and last, include two activities per day.
Include wellness tips and benefits for each activity, and should be an attribute under each activity. The first activity should be related to arrival and check in, but don't include any specific accommodation.
The last activity should be departure, so returning to the airport and returning to {flightFrom}. Transportation should be included for each activity.
The json attributes under each date should be activities, and attributes in activities should be activity name, location, travel, dining, and wellness.
Only give one option for dining per activity.
"""

itinerary_prompt, itinerary_parser = create_structured_prompt(itinerary_template, itinerary_schemas)
itinerary_chain = LLMChain(llm=chat, prompt=itinerary_prompt)
