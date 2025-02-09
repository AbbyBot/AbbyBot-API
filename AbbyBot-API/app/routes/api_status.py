from flask import Blueprint, jsonify
from datetime import datetime
from flasgger import swag_from

status_bp = Blueprint('status', __name__)

@status_bp.route('/status', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'responses': {
        200: {
            'description': 'API status retrieved successfully',
            'examples': {
                'application/json': {
                    "message": "AbbyBot lives! <3",
                    "timestamp": "2023-10-01 12:00:00"
                }
            }
        }
    }
})
def status():
    return jsonify({
        "message": "AbbyBot lives! <3",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
