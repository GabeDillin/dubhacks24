import logging
from config import config
import os

# Ensure the logs directory exists
os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)

logger = logging.getLogger("travel_app")
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(config.LOG_FILE)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
