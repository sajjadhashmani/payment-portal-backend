from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.customers.routes import customers as customers_bp
from app.products.routes import products as products_bp
from app.invoices.routes import invoices as invoices_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(customers_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(invoices_bp)

    # Enable CORS for all routes
    CORS(app)

    return app
