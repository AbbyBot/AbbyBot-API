import os
from ..utils.db import get_db_connection

def get_current_birthday(user_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = "SELECT user_birthday FROM user_profile WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None  
    finally:
        cursor.close()
        conn.close()



def update_user_birthday(user_id, birthday_date):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            UPDATE user_profile 
            SET user_birthday = %s 
            WHERE user_id = %s;
        """
        cursor.execute(query, (birthday_date, user_id))
        conn.commit() 
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()


def toggle_birthday(guild_id, activated_birthday):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        
        current_events = get_current_toggle_birthday(guild_id)
        if current_events == activated_birthday:
            return -1  


        query = """
            UPDATE server_settings 
            SET activated_birthday = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (activated_birthday, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_toggle_birthday(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()
    
    try:
        query = "SELECT activated_birthday FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()

def set_birthday_channel(guild_id, birthday_channel):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        
        current_birthday_channel = get_current_birthday_channel(guild_id)
        if current_birthday_channel == birthday_channel:
            return -1 

        query = """
            UPDATE server_settings 
            SET birthday_channel = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (birthday_channel, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_birthday_channel(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()
    
    try:
        query = "SELECT birthday_channel FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()