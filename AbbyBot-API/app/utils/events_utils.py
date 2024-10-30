from ..utils.db import get_db_connection

def get_current_event_value(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT activated_events FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()


def toggle_events(guild_id, activated_events):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_events = get_current_event_value(guild_id)
        if current_events == activated_events:
            return -1  

        query = """
            UPDATE server_settings 
            SET activated_events = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (activated_events, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()