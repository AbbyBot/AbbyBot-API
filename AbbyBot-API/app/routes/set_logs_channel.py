from flask import Blueprint, jsonify, request
from ..utils.logs_channel_utils import set_logs_channel

set_logs_channel_bp = Blueprint('set_logs_channel', __name__)

@set_logs_channel_bp.route('/set-logs_channel', methods=['POST'])
def change_logs_channel():

    guild_id = request.json.get('guild_id')
    logs_channel = request.json.get('logs_channel')

    # Check if logs_channel is a number
    if not isinstance(logs_channel, (int, str)) or not str(logs_channel).isdigit():
        return jsonify({"error": "Invalid value for logs_channel. It must be a numeric value.", "status_code": 400}), 400

    # Convert logs_channel to int if it is a numeric string
    birthday_channel = int(logs_channel)

    rows_affected = set_logs_channel(guild_id, logs_channel)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the logs_channel value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Changed logs_channel for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404