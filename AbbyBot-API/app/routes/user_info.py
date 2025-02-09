from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.user_info_utils import get_user_info

user_info_bp = Blueprint('user_info', __name__)

@user_info_bp.route('/user-info', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Servers'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The ID of the user to retrieve information for'
        }
    ],
    'responses': {
        200: {
            'description': 'User information retrieved successfully',
            'examples': {
                'application/json': {
                    "discord_username": "example_user",
                    "account_created_at": "2021-01-01T00:00:00Z",
                    "user_id": "123456789",
                    "user_birthday": "2000-01-01",
                    "servers_shared": 5,
                    "privilege": "Admin",
                    "theme": {
                        "theme_id": 1,
                        "theme_name": "Dark Mode",
                        "theme_class": "dark-mode"
                    }
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
def user_info():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    user_data = get_user_info(user_id)

    if user_data:
        birthday = user_data["birthday"]
        if birthday:
            birthday = birthday.strftime('%Y-%m-%d')  
        else:
            birthday = None  

        return jsonify({
            "discord_username": user_data["discord_username"],
            "account_created_at": user_data["account_created_at"] or "No data available",
            "user_id": str(user_data["user_id"]),
            "user_birthday": birthday,  
            "servers_shared": user_data["servers_shared"],
            "privilege": user_data["privilege"],
            "theme": {
                "theme_id": user_data["theme_id"],
                "theme_name": user_data["theme_name"],
                "theme_class": user_data["theme_class"]
            }
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404