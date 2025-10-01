import mysql.connector
import pandas as pd

movies = pd.read_csv('../ml-latest/movies.csv')

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
)
cur = conn.cursor()

create_movies_table_query = """
CREATE TABLE IF NOT EXISTS movies(
    movieId INT PRIMARY KEY,
    title VARCHAR(500),
    genres VARCHAR(500)
)
"""

cur.execute(create_movies_table_query)

sql = "INSERT INTO movies (movieId, title, genres) VALUES (%s, %s, %s)"
cur.executemany(sql, movies.values.tolist())

conn.commit()