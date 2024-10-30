from ..utils.db import get_db_connection

def get_current_language(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT guild_language FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()



def update_language(guild_id, guild_language):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_language = get_current_language(guild_id)
        if current_language == guild_language:
            return -1  


        query = """
            UPDATE server_settings 
            SET guild_language = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (guild_language, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()