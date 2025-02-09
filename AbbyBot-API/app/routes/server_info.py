from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from flasgger import swag_from
from ..utils.server_info_utils import get_server_info
import json

load_dotenv()

server_info_bp = Blueprint('server_info', __name__)

@server_info_bp.route('/server-info', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Servers'],
    'parameters': [
        {
            'name': 'guild_id',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The ID of the guild'
        }
    ],
    'responses': {
        200: {
            'description': 'A JSON object containing the server information',
            'examples': {
                'application/json': {
                    "guild_id": "123456789",
                    "guild_name": "Example Guild",
                    "member_count": 100,
                    "prefix": "!",
                    "activated_events": True,
                    "activated_logs": True,
                    "activated_birthday": True,
                    "birthday_channel": "123456789",
                    "logs_channel": "123456789",
                    "guild_language": "English",
                    "default_role_id": "123456789",
                    "default_bot_role_id": "123456789",
                    "guild_icon_url": "http://example.com/icon.png",
                    "activated_join_channel": True,
                    "activated_kick_channel": True,
                    "activated_ban_channel": True,
                    "join_channel_id": "123456789",
                    "kick_channel_id": "123456789",
                    "ban_channel_id": "123456789",
                    "owner_username": "owner"
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'examples': {
                'application/json': {
                    "error": "guild_id is required"
                }
            }
        }
    }
})
def list_photos():
    guild_id = request.args.get('guild_id')
    if not guild_id:
        return jsonify({"error": "guild_id is required"}), 400

    server_info = get_server_info(guild_id)
    return jsonify(json.loads(server_info))
