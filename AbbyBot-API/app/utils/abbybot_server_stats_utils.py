import os
from ..utils.db import get_db_connection

def get_all_server_stats():
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            select 
            (select count(guild_id) from server_settings) as 'servers_using_abbybot',
            (select count(user_id) from user_profile) as 'users_served',
            (select sum(xp_total) from user_profile) as 'xp_earned';
            """
        cursor.execute(query)
        results = cursor.fetchall()
        formatted_results = [
            {
                "servers_using_abbybot": row[0],
                "users_served": row[1],
                "xp_earned": row[2]
            }
            for row in results
        ]
        return formatted_results
    finally:
        cursor.close()
        conn.close()


def get_all_privileges():
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            SELECT privilege_name,
            value, rol_meaning,
            how_to_get, xp_multiplier,
            exclusive_access FROM privileges;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        formatted_results = [
            {
                "privilege_name": row[0],
                "value": row[1],
                "rol_meaning": row[2],
                "how_to_get": row[3],
                "xp_multiplier": row[4],
                "exclusive_access": row[5]
            }
            for row in results
        ]
        return formatted_results
    finally:
        cursor.close()
        conn.close()

