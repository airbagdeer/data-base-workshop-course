import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

load_dotenv()

# Create a connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="movie_pool",
    pool_size=5,  # Adjust based on your needs
    pool_reset_session=True,
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )
    return conn
