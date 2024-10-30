from flask import Blueprint, jsonify, request
from ..utils.db import get_db_connection, get_server_count

bot_info_bp = Blueprint('bot_info', __name__)

@bot_info_bp.route('/bot-info', methods=['GET', 'POST'])
def bot_info():
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        query = "SELECT * FROM bot_info LIMIT 1"
        cursor.execute(query)
        bot_info = cursor.fetchone()

        cursor.close()
        conn.close()

        if bot_info:
            server_count = get_server_count()
            return jsonify({
                "bot_id": bot_info["bot_id"],
                "bot_name": bot_info["bot_name"],
                "discriminator": bot_info["discriminator"],
                "avatar_url": bot_info["avatar_url"],
                "banner_url": bot_info["banner_url"],
                "server_count": server_count,
                "version": bot_info["version"],
                "version_code": bot_info["version_code"],
                "status": bot_info.get("status", "unknown")
            })
        else:
            return jsonify({"error": "No bot information found"}), 404

    elif request.method == 'POST':
        try:
            data = request.json
            bot_status = data.get("status")
            
            if bot_status not in ["online", "offline"]:
                return jsonify({"error": "Invalid status value"}), 400

            cursor.execute("SELECT bot_id FROM bot_info LIMIT 1")
            bot_info = cursor.fetchone()

            if bot_info:
                bot_id = bot_info["bot_id"]
                update_query = """
                    UPDATE bot_info 
                    SET status = %s 
                    WHERE bot_id = %s
                """
                cursor.execute(update_query, (bot_status, bot_id))
                conn.commit()

                cursor.close()
                conn.close()

                return jsonify({"message": f"Bot status updated to {bot_status}"}), 200
            else:
                return jsonify({"error": "No bot information found"}), 404
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({"error": str(e)}), 500
