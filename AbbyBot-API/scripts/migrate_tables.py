import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db_connection

def execute_sql_script(file_path, database):
    conn = get_db_connection(database)
    cursor = conn.cursor()

    with open(file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    for statement in sql_script.split(';'):
        if statement.strip():
            cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_dotenv()

    try:
        database_name = os.getenv('DB_API_NAME')
        if not database_name:
            raise ValueError("Environment variable 'DB_API_NAME' is not set.")
    except Exception as e:
        print(f"Error retrieving database name: {e}")
        sys.exit(1)

    try:
        sql_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'sql', 'create_tables.sql'
        )
        if not os.path.exists(sql_file_path):
            raise FileNotFoundError(f"SQL file not found at path: {sql_file_path}")
    except Exception as e:
        print(f"Error retrieving SQL file path: {e}")
        sys.exit(1)

    execute_sql_script(sql_file_path, database_name)
    print("\033[92mDatabase migration completed successfully!\033[0m")
