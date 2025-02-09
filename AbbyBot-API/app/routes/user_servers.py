from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.db import get_user_server_data
from ..utils.user_info_utils import get_user_info

user_servers_bp = Blueprint('user_servers', __name__)

@user_servers_bp.route('/user-servers', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Servers'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The ID of the user'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of servers the user is part of',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'string'},
                    'servers': {'type': 'array', 'items': {'type': 'object'}}
                }
            }
        },
        400: {
            'description': 'No user_id provided'
        },
        404: {
            'description': 'No data found for this user'
        }
    }
})
def user_servers():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    user_data = get_user_server_data(user_id)
    user_info = get_user_info(user_id)

    if user_data and user_info:
        return jsonify({
            "user_id": str(user_id),
            "servers": user_data
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404
