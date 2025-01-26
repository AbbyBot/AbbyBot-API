from ..utils.db import get_db_connection
import os
import json

def get_server_info(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            SELECT 
                ss.guild_id,
                ss.guild_name,
                ss.member_count,
                ss.prefix,
                ss.activated_events,
                ss.activated_logs,
                ss.activated_birthday,
                ss.birthday_channel,
                ss.logs_channel,
                l.language_name AS guild_language,
                ss.default_role_id,
                ss.default_bot_role_id,
                ss.guild_icon_url,
                ss.activated_join_channel,
                ss.activated_kick_channel,
                ss.activated_ban_channel,
                ss.join_channel_id,
                ss.kick_channel_id,
                ss.ban_channel_id,
                up.user_username AS owner_username
            FROM 
                server_settings ss
            LEFT JOIN 
                languages l ON ss.guild_language = l.id
            LEFT JOIN 
                user_profile up ON ss.owner_id = up.user_id
            WHERE guild_id = %s;
        """
        cursor.execute(query, (guild_id,))
        result = cursor.fetchall()
        formated_result = [
            {
                "guild_id": row[0],
                "guild_name": row[1],
                "member_count": row[2],
                "prefix": row[3],
                "activated_events": row[4],
                "activated_logs": row[5],
                "activated_birthday": row[6],
                "birthday_channel": row[7],
                "logs_channel": row[8],
                "guild_language": row[9],
                "default_role_id": row[10],
                "default_bot_role_id": row[11],
                "guild_icon_url": row[12],
                "activated_join_channel": row[13],
                "activated_kick_channel": row[14],
                "activated_ban_channel": row[15],
                "join_channel_id": row[16],
                "kick_channel_id": row[17],
                "ban_channel_id": row[18],
                "owner_username": row[19]
            }
            for row in result
        ]
    finally:
        cursor.close()
        conn.close()

    return json.dumps(formated_result)