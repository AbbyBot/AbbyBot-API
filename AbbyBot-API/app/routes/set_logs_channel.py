from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.logs_channel_utils import set_logs_channel

set_logs_channel_bp = Blueprint('set_logs_channel', __name__)

@set_logs_channel_bp.route('/set-logs_channel', methods=['POST'])
@swag_from({
    'tags': ['AbbyBot Servers'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'guild_id': {
                        'type': 'string',
                        'description': 'The ID of the guild'
                    },
                    'logs_channel': {
                        'type': 'string',
                        'description': 'The ID of the logs channel'
                    }
                },
                'required': ['guild_id', 'logs_channel']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Logs channel updated successfully',
            'examples': {
                'application/json': {
                    'success': 'Changed logs_channel for guild {guild_id}',
                    'status_code': 200
                }
            }
        },
        '400': {
            'description': 'Invalid value for logs_channel',
            'examples': {
                'application/json': {
                    'error': 'Invalid value for logs_channel. It must be a numeric value.',
                    'status_code': 400
                }
            }
        },
        '404': {
            'description': 'No guild found with the provided guild_id',
            'examples': {
                'application/json': {
                    'error': 'No guild found with the provided guild_id',
                    'status_code': 404
                }
            }
        }
    }
})
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