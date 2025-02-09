from flask import Blueprint, jsonify, request
from ..utils.server_settings_utils import update_language

server_settings_bp = Blueprint('server_settings', __name__)

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
