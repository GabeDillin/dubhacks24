# utils/llm.py

from langchain_community.chat_models import ChatPerplexity
from config import Config

# Initialize the LLM instance
llm = ChatPerplexity(
    temperature=0.4,
    model="llama-3.1-sonar-small-128k-online",
    pplx_api_key=Config.PERPLEXITY_API_KEY
)
