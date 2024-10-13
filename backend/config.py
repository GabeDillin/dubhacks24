# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

class Config:
    # API Keys
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
    AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
    
    # Other Configurations
    DEBUG = False
    LOG_FILE = 'logs/app.log'

config = Config()