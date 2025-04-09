from flask import Blueprint, jsonify, request
import os
from flasgger import swag_from
from ..utils.bot_info_utils import get_bot_info, update_bot_status

bot_info_bp = Blueprint('bot_info', __name__)

@bot_info_bp.route('/bot-info', methods=['GET', 'POST'])
@swag_from({
    'tags': ['Health'],
    'responses': {
        200: {
            'description': 'Bot information updated successfully',
            'examples': {
                'application/json': {
                    "message": "Bot information updated successfully"
                }
            }
        },
        404: {
            'description': 'No bot information found',
            'examples': {
                'application/json': {
                    "error": "No bot information found"
                }
            }
        },
        400: {
            'description': 'Invalid input data',
            'examples': {
                'application/json': {
                    "error": "Invalid input data",
                    "modifiable_fields": ["avatar_url", "bot_id", "bot_name", "discriminator", "server_count", "status", "version"]
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'examples': {
                'application/json': {
                    "error": "Internal server error"
                }
            }
        }
    }
})
def bot_info():
    if request.method == 'GET':
        bot_info = get_bot_info()
        if bot_info:
            return jsonify(bot_info)
        else:
            return jsonify({"error": "No bot information found"}), 404

    elif request.method == 'POST':
        try:
            if not request.is_json:
                return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

            data = request.json
            if not data:
                return jsonify({
                    "error": "Invalid input data",
                    "modifiable_fields": ["avatar_url", "bot_id", "bot_name", "discriminator", "server_count", "status", "version"]
                }), 400

            allowed_fields = ["avatar_url", "bot_id", "bot_name", "discriminator", "server_count", "status", "version"]
            update_data = {key: value for key, value in data.items() if key in allowed_fields}

            if not update_data:
                return jsonify({
                    "error": "Invalid input data",
                    "modifiable_fields": allowed_fields
                }), 400

            if update_bot_status(update_data):
                return jsonify({"message": "Bot information updated successfully"}), 200
            else:
                return jsonify({"error": "No bot information found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
