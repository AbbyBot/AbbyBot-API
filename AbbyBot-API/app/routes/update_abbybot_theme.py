from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.theme_utils import update_abbybot_theme, theme_exists

update_abbybot_theme_bd = Blueprint('update_birthday', __name__)

@update_abbybot_theme_bd.route('/update-abbybot_theme', methods=['POST'])
@swag_from({
    'tags': ['AbbyBot Themes'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {
                        'type': 'string',
                        'description': 'The ID of the user'
                    },
                    'theme_id': {
                        'type': 'string',
                        'description': 'The ID of the theme'
                    }
                },
                'required': ['user_id', 'theme_id']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Theme updated successfully',
            'examples': {
                'application/json': {
                    'success': 'AbbyBot_theme updated for user {user_id}',
                    'status_code': 200
                }
            }
        },
        '400': {
            'description': 'Invalid input or theme_id',
            'examples': {
                'application/json': {
                    'error': 'Missing user_id or theme_id',
                    'status_code': 400
                }
            }
        },
        '404': {
            'description': 'User not found',
            'examples': {
                'application/json': {
                    'error': 'No user found with the provided user_id',
                    'status_code': 404
                }
            }
        }
    }
})
def update_theme():
    user_id = request.json.get('user_id')
    theme_id = request.json.get('theme_id')

    if not user_id or not theme_id:
        return jsonify({"error": "Missing user_id or theme_id", "status_code": 400}), 400

    if not theme_exists(theme_id):
        return jsonify({"error": "Invalid theme_id", "status_code": 400}), 400

    rows_affected = update_abbybot_theme(user_id, theme_id)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the theme is already set to this value", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"AbbyBot_theme updated for user {user_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No user found with the provided user_id", "status_code": 404}), 404