# app.py

from flask import Flask
from routes import trip_info_route
from utils.logger import logger

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(trip_info_route)

    @app.route('/')
    def index():
        return "Travel App is running."

    return app

app = create_app()
