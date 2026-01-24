import os
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import subprocess

def init_db_from_dump(dump_file_path):
    load_dotenv()
    
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')
    port = os.getenv('DB_PORT', '3306')
    
    if not all([user, password, database]):
        raise ValueError("Missing required environment variables: DB_USER, DB_PASSWORD, DB_NAME")
    
    if not os.path.exists(dump_file_path):
        raise FileNotFoundError(f"Dump file not found: {dump_file_path}")
    
    print(f"Connecting to MySQL server at {host}:{port}...")
    
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Drop existing database if it exists
            print(f"Dropping database '{database}' if it exists...")
            cursor.execute(f"DROP DATABASE IF EXISTS `{database}`")
            
            # Create fresh database
            print(f"Creating database '{database}'...")
            cursor.execute(f"CREATE DATABASE `{database}`")
            
            cursor.close()
            connection.close()
            print(f"Database '{database}' recreated successfully.")
            
            # Load dump file using mysql command
            print(f"Loading dump file: {dump_file_path}")
            
            # Construct mysql command
            mysql_cmd = [
                'mysql',
                f'--host={host}',
                f'--user={user}',
                f'--password={password}',
                f'--port={port}',
                database
            ]
            
            # Execute mysql command with dump file as input
            with open(dump_file_path, 'r') as dump_file:
                result = subprocess.run(
                    mysql_cmd,
                    stdin=dump_file,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0:
                print(f"✓ Dump loaded successfully into '{database}'!")
            else:
                print(f"✗ Error loading dump:")
                print(result.stderr)
                sys.exit(1)
                
    except Error as e:
        print(f"MySQL Error: {e}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running mysql command: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python init_db_from_dump.py <path_to_dump_file>")
        sys.exit(1)
    
    dump_path = sys.argv[1]
    init_db_from_dump(dump_path)