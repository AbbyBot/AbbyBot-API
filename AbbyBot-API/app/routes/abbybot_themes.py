from flask import Blueprint, jsonify
from flasgger import swag_from
from ..utils.theme_utils import get_themes_data

abbybot_themes_bp = Blueprint('abbybot_themes', __name__)

@abbybot_themes_bp.route('/abbybot-themes', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Themes'],
    'responses': {
        200: {
            'description': 'A list of AbbyBot themes',
            'schema': {
                'type': 'object',
                'properties': {
                    'abbybot_themes': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'theme_id': {'type': 'integer'},
                                'theme_title': {'type': 'string'},
                                'theme_class': {'type': 'string'}
                            }
                        }
                    }
                },
                'example': {
                    "abbybot_themes": [
                        {
                            "theme_id": 1,
                            "theme_title": "Abby",
                            "theme_class": "abby-theme"
                        },
                        {
                            "theme_id": 2,
                            "theme_title": "D0Z3R",
                            "theme_class": "d0z3r-theme"
                        }
                    ]
                }
            }
        },
        404: {
            'description': 'No data found for this user'
        }
    }
})
def get_all_themes():
    themes_data = get_themes_data()
    if themes_data:
        return jsonify({
            "abbybot_themes": [
                {
                    "theme_id": theme["id"],
                    "theme_title": theme["title"],
                    "theme_class": theme["theme_class"]
                } for theme in themes_data
            ]
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404