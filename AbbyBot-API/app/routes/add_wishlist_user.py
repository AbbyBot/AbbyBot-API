from flask import Blueprint, request, jsonify
from ..utils.wishlist_utils import add_wishlist
from flasgger import swag_from

add_wishlist_bp = Blueprint('add_wishlist', __name__)

@add_wishlist_bp.route('/add-wishlist', methods=['POST'])
@swag_from({
    'tags': ['Wishlist'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'discord_username': {'type': 'string'},
                    'reason': {'type': 'string', 'nullable': True},
                    'how_learned': {'type': 'string', 'nullable': True}
                },
                'required': ['name', 'email', 'discord_username'],
                'example': {
                    'name': 'John Doe',
                    'email': 'john.doe@example.com',
                    'discord_username': 'johndoe#1234',
                    'reason': 'I love this bot!',
                    'how_learned': 'Through a friend'
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Wishlist item added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'status_code': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Invalid input or missing required fields',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'status_code': {'type': 'integer'}
                }
            }
        },
        '500': {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'status_code': {'type': 'integer'}
                }
            }
        }
    }
})
def handle_add_wishlist():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided", "status_code": 400}), 400

    # Check obligatory fields
    if 'name' not in data or 'email' not in data or 'discord_username' not in data:
        return jsonify({"error": "Missing required fields", "status_code": 400}), 400

    # Collect optional fields or assign None if they are not present
    name = data.get('name')
    email = data.get('email')
    discord_username = data.get('discord_username')
    reason = data.get('reason', None)  # use None as default value if the key is not present
    how_learned = data.get('how_learned', None)

    try:
        response = add_wishlist(name, email, discord_username, reason, how_learned)
        if "success" in response:
            return jsonify({"message": response, "status_code": 201}), 201
        else:
            return jsonify({"error": response, "status_code": 400}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500
