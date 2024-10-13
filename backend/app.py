# app.py
from flask import Flask
from flask_cors import CORS

from routes import trip_info_route
from utils.logger import logger

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(trip_info_route)

if __name__ == '__main__':
    app.run(debug=False)
