from flask import Blueprint, jsonify, request
from ..utils.logs_utils import toggle_logs

toggle_logs_bp = Blueprint('toggle_logs', __name__)


@toggle_logs_bp.route('/toggle-logs', methods=['POST'])
def toggle_auto_logs():

    guild_id = request.json.get('guild_id')
    activated_logs = request.json.get('activated_logs')
    

    if not isinstance(activated_logs, int):
        return jsonify({"error": "Invalid value for activated_logs. It must be a number (0 or 1).", "status_code": 400}), 400
  
    

    if activated_logs not in [0, 1]:
        return jsonify({"error": "Invalid value for activated_logs. It must be 0 or 1.", "status_code": 400}), 400


    rows_affected = toggle_logs(guild_id, activated_logs)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the activated_events value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        if activated_logs == 1:
            return jsonify({"success": f"Activated logs for guild {guild_id}", "status_code": 200}), 200
        else:
            return jsonify({"success": f"Deactivated logs for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404