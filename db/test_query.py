import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234567890',
    database='movies_db'
)

cursor = conn.cursor(dictionary=True)

# Test the exact query from the backend
try:
    cursor.execute("""
        SELECT p.id, p.name, p.gender, p.profile_path, c.character_name as character, c.order_index as cast_order
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        WHERE c.movie_id = %s
        ORDER BY c.order_index
    """, (197,))
    
    results = cursor.fetchall()
    print("=== QUERY SUCCESSFUL ===")
    print(f"Found {len(results)} cast members")
    for i, row in enumerate(results[:3]):
        print(f"\n{i+1}. {row}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

cursor.close()
conn.close()
