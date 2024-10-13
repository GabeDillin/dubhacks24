# run.py

from app import app
from utils.logger import logger

if __name__ == '__main__':
    logger.info("Starting the Travel App...")
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug=False in production
