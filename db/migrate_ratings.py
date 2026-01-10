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

print("=== Starting Ratings Table Migration ===\n")

# Step 1: Add user_id column
print("1. Adding user_id column...")
try:
    cursor.execute("""
        ALTER TABLE ratings 
        ADD COLUMN user_id VARCHAR(255) DEFAULT 'legacy_user'
    """)
    print("   ✓ user_id column added")
except Exception as e:
    print(f"   ⚠ Error (may already exist): {e}")

# Step 2: Change rating from FLOAT to INT
print("\n2. Changing rating column from FLOAT to INT...")
try:
    # First, round existing ratings to integers
    cursor.execute("UPDATE ratings SET rating = ROUND(rating)")
    cursor.execute("ALTER TABLE ratings MODIFY COLUMN rating INT NOT NULL")
    print("   ✓ rating column changed to INT")
except Exception as e:
    print(f"   ⚠ Error: {e}")

# Step 3: Add unique constraint on (movie_id, user_id)
print("\n3. Adding UNIQUE constraint on (movie_id, user_id)...")
try:
    cursor.execute("""
        ALTER TABLE ratings 
        ADD CONSTRAINT unique_user_movie_rating 
        UNIQUE (movie_id, user_id)
    """)
    print("   ✓ UNIQUE constraint added")
except Exception as e:
    print(f"   ⚠ Error (may already exist): {e}")

# Step 4: Add index on user_id
print("\n4. Adding index on user_id...")
try:
    cursor.execute("CREATE INDEX idx_user_id ON ratings(user_id)")
    print("   ✓ Index on user_id created")
except Exception as e:
    print(f"   ⚠ Error (may already exist): {e}")

# Commit changes
conn.commit()

# Verify the changes
print("\n=== Verifying Migration ===\n")
cursor.execute("DESCRIBE ratings")
print("Updated table structure:")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== Migration Complete ===")

cursor.close()
conn.close()
