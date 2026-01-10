import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
    cursor = conn.cursor(dictionary=True)
    
    print("=== Testing Movies Query ===")
    query = "SELECT * FROM movies LIMIT 2"
    cursor.execute(query)
    movies = cursor.fetchall()
    
    print(f"Found {len(movies)} movies")
    for movie in movies:
        print(f"  - {movie['title']} (ID: {movie['id']})")
    
    print("\n=== Testing Ratings Table ===")
    cursor.execute("SELECT * FROM ratings LIMIT 3")
    ratings = cursor.fetchall()
    print(f"Found {len(ratings)} ratings")
    for rating in ratings:
        print(f"  - Movie {rating['movie_id']}: {rating['rating']} by {rating['user_id']}")
    
    cursor.close()
    conn.close()
    print("\n✓ Database connection and queries working fine")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
