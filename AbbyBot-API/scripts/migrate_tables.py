import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db_connection

MAX_RETRIES = 10
WAIT_SECONDS = 3

def execute_sql_script(file_path, database):
    attempt = 1
    while attempt <= MAX_RETRIES:
        try:
            print(f"🔄 Trying to connect to the database (attempt {attempt}/{MAX_RETRIES})...")
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

            print("\033[92m✅ Migration completed successfully!\033[0m")
            return
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            if attempt == MAX_RETRIES:
                print("\033[91m🔥 Failed to connect to the database after multiple attempts. Aborting.\033[0m")
                sys.exit(1)
            attempt += 1
            time.sleep(WAIT_SECONDS)

if __name__ == "__main__":
    try:
        database_name = os.getenv('DB_API_NAME')
        if not database_name:
            raise ValueError("The environment variable 'DB_API_NAME' is not defined.")
    except Exception as e:
        print(f"Error retrieving the database name: {e}")
        sys.exit(1)

    try:
        sql_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'sql', 'create_tables.sql'
        )
        if not os.path.exists(sql_file_path):
            raise FileNotFoundError(f"SQL file not found at: {sql_file_path}")
    except Exception as e:
        print(f"Error getting the path to the SQL file: {e}")
        sys.exit(1)

    execute_sql_script(sql_file_path, database_name)
