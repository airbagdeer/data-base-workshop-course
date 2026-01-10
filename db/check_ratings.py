import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = conn.cursor()

# Show all tables
cursor.execute('SHOW TABLES')
tables = cursor.fetchall()
print('=== ALL TABLES ===')
for table in tables:
    print(table[0])

# Check if ratings table exists
print('\n=== RATINGS TABLE STRUCTURE ===')
try:
    cursor.execute('DESCRIBE ratings')
    for row in cursor.fetchall():
        print(row)
    
    # Check sample data
    print('\n=== SAMPLE RATINGS DATA ===')
    cursor.execute('SELECT * FROM ratings LIMIT 5')
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    print(f"Error: {e}")

cursor.close()
conn.close()
