from flask import Blueprint, jsonify, request
from ..utils.birthday_utils import toggle_birthday

toggle_automatic_events_bp = Blueprint('toggle_automatic_events', __name__)


@toggle_automatic_events_bp.route('/toggle_automatic_events', methods=['POST'])
def toggle_automatic_event():

    guild_id = request.json.get('guild_id')
    activated_events = request.json.get('activated_events')
    

    if not isinstance(activated_events, int):
        return jsonify({"error": "Invalid value for activated_events. It must be a number (0 or 1).", "status_code": 400}), 400
  
    

    if activated_events not in [0, 1]:
        return jsonify({"error": "Invalid value for activated_events. It must be 0 or 1.", "status_code": 400}), 400


    rows_affected = toggle_birthday(guild_id, activated_events)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the activated_events value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        if activated_events == 1:
            return jsonify({"success": f"Activated auto events for guild {guild_id}", "status_code": 200}), 200
        else:
            return jsonify({"success": f"Deactivated auto events for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404
    
