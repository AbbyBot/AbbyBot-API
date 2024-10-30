import mysql.connector
import os

def get_db_connection(database):
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=database
    )

def get_server_count():
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT guild_id) FROM dashboard;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count
