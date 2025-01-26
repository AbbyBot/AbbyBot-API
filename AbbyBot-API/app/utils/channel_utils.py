import os
from ..utils.db import get_db_connection

# Join channel

def get_current_join_channel(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = "SELECT join_channel_id FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]
    finally:
        cursor.close()
        conn.close()

def update_join_channel(guild_id, join_channel_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            UPDATE server_settings 
            SET join_channel_id = %s
            WHERE guild_id = %s;
        """
        cursor.execute(query, (join_channel_id, guild_id))
        conn.commit() 
        return cursor.rowcount  
    finally:
        cursor.close()
        conn.close()
def set_join_channel_id(guild_id, join_channel_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        current_join_channel = get_current_join_channel(guild_id)
        if current_join_channel == join_channel_id:
            return -1  

        query = """
            UPDATE server_settings 
            SET join_channel_id = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (join_channel_id if join_channel_id is not None else None, guild_id))  
        conn.commit()  
        return cursor.rowcount  
    finally:
        cursor.close()
        conn.close()

# Kick channel

def get_current_kick_channel(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = "SELECT kick_channel_id FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]
    finally:
        cursor.close()
        conn.close()

def update_kick_channel(guild_id, kick_channel_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            UPDATE server_settings 
            SET kick_channel_id = %s
            WHERE guild_id = %s;
        """
        cursor.execute(query, (kick_channel_id, guild_id))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()

def set_kick_channel_id(guild_id, kick_channel_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        current_kick_channel = get_current_kick_channel(guild_id)
        if current_kick_channel == kick_channel_id:
            return -1  

        query = """
            UPDATE server_settings 
            SET kick_channel_id = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (kick_channel_id if kick_channel_id is not None else None, guild_id))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()


# Ban channel

def get_current_ban_channel(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = "SELECT ban_channel_id FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]
    finally:
        cursor.close()
        conn.close()

def update_ban_channel(guild_id, ban_channel_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            UPDATE server_settings 
            SET ban_channel_id = %s
            WHERE guild_id = %s;
        """
        cursor.execute(query, (ban_channel_id, guild_id))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()

def set_ban_channel_id(guild_id, ban_channel_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        current_ban_channel = get_current_ban_channel(guild_id)
        if current_ban_channel == ban_channel_id:
            return -1  

        query = """
            UPDATE server_settings 
            SET ban_channel_id = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (ban_channel_id if ban_channel_id is not None else None, guild_id))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
