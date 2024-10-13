from flask import request
from datetime import datetime
from utils.logger import logger

def parse_request_data():
    if request.is_json:
        data = request.get_json()
        required_fields = [
            'flightFrom', 'flightTo', 'flightDate',
            'flightReturnDate', 'budget', 'numAdults'
        ]
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing field: {field}")
                raise ValueError(f"Missing field: {field}")

        flight_date_obj = datetime.strptime(data['flightDate'], '%Y-%m-%d')
        flight_return_date_obj = datetime.strptime(data['flightReturnDate'], '%Y-%m-%d')
        data['duration'] = (flight_return_date_obj - flight_date_obj).days
        return data
    else:
        logger.error("Request content type must be application/json")
        raise ValueError("Request content type must be application/json")
