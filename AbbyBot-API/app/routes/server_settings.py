from flask import Blueprint, jsonify, request
from ..utils.db import get_db_connection

server_settings_bp = Blueprint('server_settings', __name__)

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

@server_settings_bp.route('/update-language', methods=['POST'])
def update_guild_language_route():
    guild_id = request.json.get('guild_id')
    language_id = request.json.get('language_id')
    
    rows_affected = update_language(guild_id, language_id)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the language is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Language updated for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404
