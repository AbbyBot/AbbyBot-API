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
            'description': 'Bot information retrieved successfully',
            'examples': {
                'application/json': {
                    "bot_id": "123456789",
                    "bot_name": "AbbyBot",
                    "discriminator": "0001",
                    "avatar_url": "http://example.com/avatar.png",
                    "banner_url": "http://example.com/banner.png",
                    "server_count": 10,
                    "version": "1.0.0",
                    "status": "online"
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
            'description': 'Invalid status value',
            'examples': {
                'application/json': {
                    "error": "Invalid status value"
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
            data = request.json
            bot_status = data.get("status")
            
            if bot_status not in ["online", "offline"]:
                return jsonify({"error": "Invalid status value"}), 400

            if update_bot_status(bot_status):
                return jsonify({"message": f"Bot status updated to {bot_status}"}), 200
            else:
                return jsonify({"error": "No bot information found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
