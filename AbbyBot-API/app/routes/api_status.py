from flask import Blueprint, jsonify
from datetime import datetime

status_bp = Blueprint('status', __name__)

@status_bp.route('/status', methods=['GET'])
def status():
    return jsonify({
        "message": "AbbyBot lives! <3",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
