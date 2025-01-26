from ..utils.db import get_db_connection
import os

def set_prefix(guild_id, prefix):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        
        current_events_logs = get_current_prefix(guild_id)
        if current_events_logs == prefix:
            return -1 


        query = """
            UPDATE server_settings 
            SET prefix = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (prefix, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_prefix(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()
    
    try:
        query = "SELECT prefix FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()