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

def get_user_server_data(user_id):
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT s.guild_id, s.guild_name, s.owner_id, d.is_admin, s.guild_icon_url, s.guild_icon_last_updated,
    s.activated_events, s.activated_logs, s.activated_birthday, s.birthday_channel, s.logs_channel,
    s.guild_language, s.default_bot_role_id, s.default_role_id, s.join_channel_id, s.kick_channel_id, s.ban_channel_id 
    FROM dashboard d
    JOIN server_settings s ON d.guild_id = s.guild_id
    JOIN user_profile up ON d.user_profile_id = up.id
    LEFT JOIN privileges p ON up.user_privilege = p.id
    WHERE up.user_id = %s;
    """
    
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    if result:
        user_id_int = int(user_id)

        for server in result:
            server['guild_id'] = str(server['guild_id'])
            server['is_owner'] = 1 if server['owner_id'] == user_id_int else 0
            if server['guild_icon_url']:
                server['guild_icon_url']

        return result
    else:
        return None