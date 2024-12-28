import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the application."""

    # Database configuration
    DB_NAME = os.getenv("DB_NAME", "postgres")  # Default to 'postgres' if not set
    DB_USER = os.getenv("DB_USER", "postgres")  # Default to 'postgres' if not set
    DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")  # Default to 'admin' if not set
    DB_HOST = os.getenv("DB_HOST", "localhost")  # Default to 'localhost' if not set
    DB_PORT = os.getenv("DB_PORT", "5432")  # Default to '5432' if not set
