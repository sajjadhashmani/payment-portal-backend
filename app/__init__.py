from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.customers.routes import customers as customers_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(customers_bp)

    # Enable CORS for all routes
    CORS(app)

    return app
