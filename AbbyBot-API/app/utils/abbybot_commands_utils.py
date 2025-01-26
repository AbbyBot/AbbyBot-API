from ..utils.db import get_db_connection
import os

def get_commands_by_category(category_name, language_id=1):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            SELECT `command_code`, `command_description`, `usage`
            FROM `help`
            WHERE `category_id` = (
                SELECT `id`
                FROM `help_categories`
                WHERE `category_name` = %s
            ) AND `language_id` = %s;
        """
        cursor.execute(query, (category_name, language_id))
        results = cursor.fetchall()
        formatted_results = [
            {
                "command": row[0],
                "description": row[1],
                "usage": row[2]
            }
            for row in results
        ]
        return formatted_results
    finally:
        cursor.close()
        conn.close()

def get_all_commands(language_id=1):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            SELECT `command_code`, `command_description`, `usage`
            FROM `help`
            WHERE `language_id` = %s;
        """
        cursor.execute(query, (language_id,))
        results = cursor.fetchall()
        formatted_results = [
            {
                "command": row[0],
                "description": row[1],
                "usage": row[2]
            }
            for row in results
        ]
        return formatted_results
    finally:
        cursor.close()
        conn.close()

def get_categories():
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor()

    try:
        query = """
            SELECT `category_name`
            FROM `help_categories`;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        formatted_results = [{"category_name": row[0]} for row in results]
        return formatted_results
    finally:
        cursor.close()
        conn.close()

def get_control_commands(language_id=1):
    return get_commands_by_category('/control', language_id)

def get_minigames_commands(language_id=1):
    return get_commands_by_category('/minigames', language_id)

def get_music_commands(language_id=1):
    return get_commands_by_category('/music', language_id)

def get_utility_commands(language_id=1):
    return get_commands_by_category('/utility', language_id)

def get_user_commands(language_id=1):
    return get_commands_by_category('/user', language_id)

def get_image_commands(language_id=1):
    return get_commands_by_category('/image', language_id)
