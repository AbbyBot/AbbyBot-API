from flask import Blueprint, request, jsonify
from flasgger import swag_from
from ..utils.server_dashboard_utils import fetch_server_dashboard

server_dashboard_bp = Blueprint('server_dashboard', __name__)

@server_dashboard_bp.route('/server-dashboard', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Servers'],
    'parameters': [
        {
            'name': 'guild_id',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The ID of the guild'
        },
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': 'The page number to fetch'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of users in the server dashboard',
            'schema': {
                'type': 'object',
                'properties': {
                    'users': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'username': {'type': 'string'},
                                'nickname_in_server': {'type': 'string'},
                                'user_type': {'type': 'string'},
                                'user_id': {'type': 'string'},
                                'server_roles': {
                                    'type': 'array',
                                    'items': {'type': 'string'}
                                },
                                'birthday_date': {'type': 'string', 'format': 'date'}
                            }
                        }
                    },
                    'total_users': {'type': 'integer'},
                    'page_users': {'type': 'integer'},
                    'page': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Missing required parameter: guild_id'
        },
        '404': {
            'description': 'guild_id not found. please provide a valid guild_id.'
        }
    }
})
def get_server_dashboard():
    guild_id = request.args.get('guild_id')
    page = request.args.get('page', 1)
    limit = 10

    if not guild_id:
        return jsonify({'error': 'Missing required parameter: guild_id'}), 400

    response_object = fetch_server_dashboard(guild_id, page, limit)
    if 'error' in response_object:
        return jsonify(response_object), 404

    return jsonify(response_object), 200
