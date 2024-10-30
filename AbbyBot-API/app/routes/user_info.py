from flask import Blueprint, jsonify, request
from ..utils.db import get_db_connection

user_info_bp = Blueprint('user_info', __name__)

def get_user_info(user_id):
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT 
            up.user_username AS discord_username, 
            up.user_birthday AS birthday,
            up.user_id, 
            up.account_created_at,  
            COALESCE(p.privilege_name, 'No privilege') AS privilege,
            (SELECT COUNT(DISTINCT guild_id) 
            FROM dashboard 
            WHERE user_profile_id = up.id) AS servers_shared,
            t.id AS theme_id,
            t.title AS theme_name,
            t.theme_class AS theme_class
        FROM user_profile up
        LEFT JOIN privileges p ON up.user_privilege = p.id
        LEFT JOIN AbbyBot_Themes t ON up.theme_id = t.id
        WHERE up.user_id = %s;
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

@user_info_bp.route('/user-info', methods=['GET'])
def user_info():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    user_data = get_user_info(user_id)

    if user_data:
        birthday = user_data["birthday"]
        if birthday:
            birthday = birthday.strftime('%Y-%m-%d')  
        else:
            birthday = None  

        return jsonify({
            "discord_username": user_data["discord_username"],
            "account_created_at": user_data["account_created_at"] or "No data available",
            "user_id": user_data["user_id"],
            "user_birthday": birthday,  
            "servers_shared": user_data["servers_shared"],
            "privilege": user_data["privilege"],
            "theme": {
                "theme_id": user_data["theme_id"],
                "theme_name": user_data["theme_name"],
                "theme_class": user_data["theme_class"]
            }
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404
