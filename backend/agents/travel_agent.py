from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor
from tools.flight_search_tool import FlightSearchTool
from tools.itinerary_creation_tool import ItineraryCreationTool
from tools.accommodation_search_tool import AccommodationSearchTool  # Assuming you're using Google Hotels API here
from langchain_community.llms import OpenAI

# Define the prompt template for the ReAct agent
react_prompt_template = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template="""
    You are a travel assistant agent with access to the following tools: flight search, accommodation search using Google Hotels API, and itinerary creation.

    Use the following format:

    Question: The input question you must answer
    Thought: You should always think about what to do
    Action: The action to take, should be one of [{tool_names}]
    Action Input: The input to the action
    Observation: The result of the action
    ... (This Thought/Action/Action Input/Observation can repeat multiple times)
    Thought: I now know the final answer
    Final Answer: The final answer to the original input question

    Begin:

    Question: {input}

    Thought:{agent_scratchpad}
    """
)

# Initialize tools
flight_search_tool = FlightSearchTool()
itinerary_creation_tool = ItineraryCreationTool()
accommodation_search_tool = AccommodationSearchTool()

# Create a list of tools for the agent
tools = [
    Tool(name="FlightSearchTool", func=flight_search_tool.run, description="Searches for flights."),
    Tool(name="ItineraryCreationTool", func=itinerary_creation_tool.run, description="Creates an itinerary."),
    Tool(name="AccommodationSearchTool", func=accommodation_search_tool.run, description="Searches for accommodations using Google Hotels API.")
]


# Create the ReAct agent
travel_agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_template
)

# Agent Executor for running the agent
travel_agent_executor = AgentExecutor(agent=travel_agent, tools=tools)

def run_agent(input_data):
    """
    Executes the ReAct agent with the provided input.
    """
    return travel_agent_executor.invoke({"input": input_data})
