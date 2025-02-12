from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.birthday_utils import set_birthday_channel

set_birthday_channel_bp = Blueprint('set_birthday_channel', __name__)

@set_birthday_channel_bp.route('/set-birthday_channel', methods=['POST'])
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
                        'description': 'ID of the guild'
                    },
                    'birthday_channel': {
                        'type': 'string',
                        'description': 'ID of the birthday channel'
                    }
                },
                'required': ['guild_id', 'birthday_channel']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Birthday channel updated successfully',
            'examples': {
                'application/json': {
                    'success': 'Changed birthday_channel for guild {guild_id}',
                    'status_code': 200
                }
            }
        },
        '400': {
            'description': 'Invalid input',
            'examples': {
                'application/json': {
                    'error': 'Invalid value for birthday_channel. It must be a numeric value.',
                    'status_code': 400
                }
            }
        },
        '404': {
            'description': 'Guild not found',
            'examples': {
                'application/json': {
                    'error': 'No guild found with the provided guild_id',
                    'status_code': 404
                }
            }
        }
    }
})
def change_birthday_channel():

    guild_id = request.json.get('guild_id')
    birthday_channel = request.json.get('birthday_channel')

    # Check if birthday_channel is a number
    if not isinstance(birthday_channel, (int, str)) or not str(birthday_channel).isdigit():
        return jsonify({"error": "Invalid value for birthday_channel. It must be a numeric value.", "status_code": 400}), 400

    # Convert birthday_channel to int if it is a numeric string
    birthday_channel = int(birthday_channel)

    rows_affected = set_birthday_channel(guild_id, birthday_channel)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the birthday_channel value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Changed birthday_channel for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404