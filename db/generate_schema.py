from pathlib import Path

from db import ROOT_DIR

SCHEMA_FILE = ROOT_DIR.joinpath('db/schema.sql')

def generate_schema(connection):
    try:
        print(f"Generating Schema")
        run_sql_script(connection, SCHEMA_FILE)
        print(f"Schema Generated")
    except Exception as e:
        print(f"Error generating schema: {e}")
        raise e

def run_sql_script(connection, sql_file_path):
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()

    statements = [statement.strip() for statement in sql_script.split(';') if statement.strip()]

    cursor = connection.cursor()
    for statement in statements:
        cursor.execute(statement)
    connection.commit()
    cursor.close()