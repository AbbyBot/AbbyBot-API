from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.prefix_utils import set_prefix

set_prefix_bp = Blueprint('set_prefix', __name__)

@set_prefix_bp.route('/set-prefix', methods=['POST'])
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
                    'prefix': {
                        'type': 'string',
                        'description': 'The new prefix to set'
                    }
                },
                'required': ['guild_id', 'prefix']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Prefix updated successfully',
            'examples': {
                'application/json': {
                    'success': 'Changed prefix for guild {guild_id}',
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
def set_new_prefix():

    guild_id = request.json.get('guild_id')
    prefix = request.json.get('prefix')
    
    rows_affected = set_prefix(guild_id, prefix)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the prefix value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Changed prefix for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404