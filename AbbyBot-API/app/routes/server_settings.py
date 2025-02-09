from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.server_settings_utils import update_language

server_settings_bp = Blueprint('server_settings', __name__)

@server_settings_bp.route('/update-language', methods=['POST'])
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
                        'description': 'The ID of the guild',
                        'example': '1234567890'
                    },
                    'language_id': {
                        'type': 'string',
                        'description': 'The new language ID to set for the guild',
                        'example': 'en'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Language updated successfully or no update needed',
            'examples': {
                'application/json': {
                    'info': 'No update needed, the language is already set',
                    'status_code': 200
                },
                'application/json': {
                    'success': 'Language updated for guild 1234567890',
                    'status_code': 200
                }
            }
        },
        404: {
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
def update_guild_language_route():
    guild_id = request.json.get('guild_id')
    language_id = request.json.get('language_id')
    
    rows_affected = update_language(guild_id, language_id)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the language is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Language updated for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404
