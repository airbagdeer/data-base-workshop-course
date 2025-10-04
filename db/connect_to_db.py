import mysql.connector

# 1) Connect without selecting a database
admin = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234567890",
)
cur = admin.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS movies")  # create schema if missing
cur.close()
admin.close()

# 2) Reconnect to the new database and run SQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234567890",
    database="movies",
    allow_local_infile=True
)
cur = conn.cursor()