import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234567890',
    database='movies_db'
)

cursor = conn.cursor()

# Check table structure
cursor.execute("DESCRIBE cast_members")
print("=== CAST_MEMBERS TABLE STRUCTURE ===")
for row in cursor.fetchall():
    print(row)

# Check sample data
cursor.execute("SELECT * FROM cast_members WHERE movie_id = 197 LIMIT 5")
print("\n=== SAMPLE CAST DATA FOR MOVIE 197 ===")
columns = [desc[0] for desc in cursor.description]
print(columns)
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
