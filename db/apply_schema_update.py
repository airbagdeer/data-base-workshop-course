from db.connect_to_db import connect_to_db

def apply_update():
    print("Connecting to database...")
    conn = connect_to_db()
    cursor = conn.cursor()
    
    print("Creating ratings table...")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS ratings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT,
        rating FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (movie_id) REFERENCES movies(id)
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    
    cursor.close()
    conn.close()
    print("Schema update applied successfully.")

if __name__ == "__main__":
    apply_update()
