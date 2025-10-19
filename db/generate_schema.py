from  connect_to_db import connect_to_db


SCHEMA_FILE = 'db/schema.sql'

def generate_schema():
    try:
        connection = connect_to_db()
        run_sql_script(connection, SCHEMA_FILE)
    except Exception as e:
        print(f"Error generating schema: {e}")
        raise e

def run_sql_script(connection, sql_file_path):
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()

    statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

    cursor = connection.cursor()
    for statement in statements:
        cursor.execute(statement)
    connection.commit()
    cursor.close()