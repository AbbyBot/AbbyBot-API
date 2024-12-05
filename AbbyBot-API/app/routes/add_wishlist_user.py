from flask import Blueprint, request, jsonify
from ..utils.wishlist_utils import add_wishlist

add_wishlist_bp = Blueprint('add_wishlist', __name__)

@add_wishlist_bp.route('/add-wishlist', methods=['POST'])
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
