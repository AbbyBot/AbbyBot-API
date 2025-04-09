import os
from ..utils.db import get_db_connection, get_server_count

def get_bot_info():
    conn = get_db_connection(os.getenv('DB_API_NAME'))
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM bot_info LIMIT 1"
    cursor.execute(query)
    bot_info = cursor.fetchone()
    cursor.close()
    conn.close()

    if bot_info:
        server_count = get_server_count()
        
        return {
            "bot_id": str(bot_info["bot_id"]),
            "bot_name": bot_info["bot_name"],
            "discriminator": bot_info["discriminator"],
            "avatar_url": bot_info["avatar_url"],
            "server_count": server_count,
            "version": bot_info["version"],
            "status": bot_info.get("status", "unknown")
        }
    
    else:
        return None

def update_bot_status(update_data):
    conn = get_db_connection(os.getenv('DB_API_NAME'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT bot_id FROM bot_info LIMIT 1")
    bot_info = cursor.fetchone()

    if bot_info:
        bot_id = str(bot_info["bot_id"])
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        update_query = f"""
            UPDATE bot_info 
            SET {set_clause} 
            WHERE bot_id = %s
        """
        cursor.execute(update_query, (*update_data.values(), bot_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False
