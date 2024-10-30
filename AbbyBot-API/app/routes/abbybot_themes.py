from flask import Blueprint, jsonify
from ..utils.theme_utils import get_themes_data

abbybot_themes_bp = Blueprint('abbybot_themes', __name__)

@abbybot_themes_bp.route('/abbybot-themes', methods=['GET'])
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