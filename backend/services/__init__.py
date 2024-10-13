# services/__init__.py

# Remove this line if it exists
# from .amadeus_service import AmadeusService

# If you need to expose functions from amadeus_service.py, you can import them here
from .amadeus_service import get_access_token, ensure_access_token, get_city_name_from_airport_code, search_flights

# Optionally, define __all__ to specify what is exported when using 'from services import *'
__all__ = [
    'get_access_token',
    'ensure_access_token',
    'get_city_name_from_airport_code',
    'search_flights',
]
