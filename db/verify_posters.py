from db.connect_to_db import connect_to_db


def verify():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM movie_posters")
    count = cursor.fetchone()[0]
    print(f"Total posters in DB: {count}")
    
    cursor.execute("SELECT movie_id, LENGTH(image) FROM movie_posters LIMIT 5")
    print("Sample poster sizes:")
    for mid, size in cursor.fetchall():
        print(f"Movie ID: {mid}, Size: {size} bytes")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    verify()
