from ..utils.db import get_db_connection
import os

class NoChannelsFoundError(Exception):
    pass

def fetch_server_channels(guild_id):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    
    try:
        with conn.cursor() as cursor:
            query = """
                    SELECT
                      id, guild_id, channel_id, channel_title 
                    FROM
                      server_channels 
                    WHERE
                      guild_id = %s;
                    """
            cursor.execute(query, (guild_id,))
            result = cursor.fetchall()

            if not result:
                raise NoChannelsFoundError(f"No channels found for guild_id: {guild_id}")

            channel_list = []
            for row in result:
                channel_data = {
                    'guild_id': str(row[1]),
                    'channel_id': str(row[2]),
                    'channel_title': row[3]
                }
                channel_list.append(channel_data)

            return channel_list

    finally:
        conn.close()
