import os
from ..utils.db import get_db_connection

def toggle_logs(guild_id, activated_logs):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        
        current_events_logs = get_current_logs_value(guild_id)
        if current_events_logs == activated_logs:
            return -1 


        query = """
            UPDATE server_settings 
            SET activated_logs = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (activated_logs, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_logs_value(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()
    
    try:
        query = "SELECT activated_logs FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()