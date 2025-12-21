import os

from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def connect_to_db():

    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD") 
    db = os.getenv("DB_NAME")
    port = int(os.getenv("DB_PORT"))

    # 1) Connect without selecting a database
    admin = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port
    )
    cur = admin.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
    cur.close()
    admin.close()

    # 2) Reconnect to the new database and run SQL
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port,
        allow_local_infile=True
    )
    return conn