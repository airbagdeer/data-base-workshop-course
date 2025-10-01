# import pandas as pd
#

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
cur.execute("CREATE TABLE IF NOT EXISTS notes(id INT PRIMARY KEY AUTO_INCREMENT, body TEXT)")
cur.execute("INSERT INTO notes(body) VALUES (%s)", ("hello world",))
conn.commit()
cur.execute("SELECT id, body FROM notes")
for row in cur.fetchall():
    print(row)
cur.close()
conn.close()
