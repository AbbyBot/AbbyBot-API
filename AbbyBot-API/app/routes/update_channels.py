from flask import Blueprint, jsonify, request
from ..utils.channel_utils import (
    get_current_join_channel, set_join_channel_id,
    get_current_kick_channel, set_kick_channel_id,
    get_current_ban_channel, set_ban_channel_id
)

update_channel_bd = Blueprint('update_channel', __name__)

# Join channel    

@update_channel_bd.route('/update-join-channel', methods=['POST'])
def update_join_channel_endpoint():
    guild_id = request.json.get('guild_id')
    join_channel_id = request.json.get('join_channel_id')

    if not guild_id:
        return jsonify({"error": "Missing guild_id", "status_code": 400}), 400

    try:
        guild_id = int(guild_id)
        join_channel_id = int(join_channel_id) if join_channel_id is not None else None
    except ValueError:
        return jsonify({"error": "Invalid guild_id or join_channel_id format. Must be an integer.", "status_code": 400}), 400

    current_join_channel = get_current_join_channel(guild_id)

    if current_join_channel is None and join_channel_id is None:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404

    rows_affected = set_join_channel_id(guild_id, join_channel_id)

    if rows_affected == -1:
        return jsonify({"success": "Join channel is already set to this value", "status_code": 200}), 200

    if rows_affected > 0:
        return jsonify({"success": f"Join channel updated for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": f"Failed to update the join channel for guild {guild_id}", "status_code": 500}), 500
    
# Kick channel    

@update_channel_bd.route('/update-kick-channel', methods=['POST'])
def update_kick_channel_endpoint():
    guild_id = request.json.get('guild_id')
    kick_channel_id = request.json.get('kick_channel_id')

    if not guild_id:
        return jsonify({"error": "Missing guild_id", "status_code": 400}), 400

    try:
        guild_id = int(guild_id)
        kick_channel_id = int(kick_channel_id) if kick_channel_id is not None else None
    except ValueError:
        return jsonify({"error": "Invalid guild_id or kick_channel_id format. Must be an integer.", "status_code": 400}), 400

    current_kick_channel = get_current_kick_channel(guild_id)

    if current_kick_channel is None and kick_channel_id is None:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404

    rows_affected = set_kick_channel_id(guild_id, kick_channel_id)

    if rows_affected == -1:
        return jsonify({"success": "Kick channel is already set to this value", "status_code": 200}), 200

    if rows_affected > 0:
        return jsonify({"success": f"Kick channel updated for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": f"Failed to update the kick channel for guild {guild_id}", "status_code": 500}), 500


# Ban channel

@update_channel_bd.route('/update-ban-channel', methods=['POST'])
def update_ban_channel_endpoint():
    guild_id = request.json.get('guild_id')
    ban_channel_id = request.json.get('ban_channel_id')

    if not guild_id:
        return jsonify({"error": "Missing guild_id", "status_code": 400}), 400

    try:
        guild_id = int(guild_id)
        ban_channel_id = int(ban_channel_id) if ban_channel_id is not None else None
    except ValueError:
        return jsonify({"error": "Invalid guild_id or ban_channel_id format. Must be an integer.", "status_code": 400}), 400

    current_ban_channel = get_current_ban_channel(guild_id)

    if current_ban_channel is None and ban_channel_id is None:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404

    rows_affected = set_ban_channel_id(guild_id, ban_channel_id)

    if rows_affected == -1:
        return jsonify({"success": "Ban channel is already set to this value", "status_code": 200}), 200

    if rows_affected > 0:
        return jsonify({"success": f"Ban channel updated for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": f"Failed to update the ban channel for guild {guild_id}", "status_code": 500}), 500



