import os
from ..utils.db import get_db_connection

def set_logs_channel(guild_id, logs_channel):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        
        current_logs_channel = get_current_logs_channel(guild_id)
        if current_logs_channel == logs_channel:
            return -1 

        query = """
            UPDATE server_settings 
            SET birthday_channel = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (logs_channel, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_logs_channel(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()
    
    try:
        query = "SELECT logs_channel FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()