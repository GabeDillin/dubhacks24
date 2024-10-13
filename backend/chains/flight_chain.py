from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema
from agents import chat, create_structured_prompt

flight_schemas = [
    ResponseSchema(name="airline", description="The name of the airline"),
    ResponseSchema(name="price", description="The price of the flight"),
    ResponseSchema(name="first_flight_depart", description="The departure time of the first flight"),
    ResponseSchema(name="first_flight_arrive", description="The arrival time of the first flight"),
    ResponseSchema(name="second_flight_depart", description="The departure time of the second flight"),
    ResponseSchema(name="second_flight_arrive", description="The arrival time of the second flight"),
    ResponseSchema(name="first_flight_number", description="The flight number of the first flight"),
    ResponseSchema(name="second_flight_number", description="The flight number of the second flight"),
    ResponseSchema(name="emissions_data", description="Emissions data for the round trip"),
]

flight_template = """
From {flightOffers}, find round-trip flights from {flightFrom} to {flightTo} for a {duration} day trip from {flightDate} to {flightReturnDate}.
The flight should be for {numAdults} adults. {flightOffers} is a json file that contains individual round-trip flights. Make sure all information matches with the specific round-trip.
Prefer to look for three flights from different carriers/airlines if all three have full information ex: no "Unknown" or "missing". If not, find three round-trips that have full information.
Do not include any round-trip twice.
List flights with arrival time and departure time with date and hour, airline for both prices, as well as price for the round trip.
Also display emissions information for each flight. The second flight information should be the return flight date and hour, not the first flight's information.
"""

flight_prompt, flight_parser = create_structured_prompt(flight_template, flight_schemas)
flight_chain = LLMChain(llm=chat, prompt=flight_prompt)
