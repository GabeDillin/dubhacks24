# agents/travel_agent.py

from langchain_community.chat_models import ChatPerplexity
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from config import Config
from utils.logger import logger

def create_structured_prompt(template, response_schemas):
    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template + "\n{format_instructions}")
    return prompt, parser

def run_chain_with_retry(chain, inputs, max_retries=3):
    
    for attempt in range(max_retries):
        print("Trying to run the model")
        try:
            # Use 'invoke' instead of 'run' if necessary
            return chain.invoke(inputs)
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise e
            logger.info("Retrying...")

# Initialize ChatPerplexity without the custom tokenizer
chat = ChatPerplexity(
    temperature=0.4,
    model="llama-3.1-sonar-small-128k-online",
    pplx_api_key=Config.PERPLEXITY_API_KEY
)
