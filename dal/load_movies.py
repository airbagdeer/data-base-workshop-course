import pandas as pd

from dal import cur, conn

movies = pd.read_csv('../ml-latest/movies.csv')


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