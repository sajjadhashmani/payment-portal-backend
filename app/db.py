import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import Config

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn
