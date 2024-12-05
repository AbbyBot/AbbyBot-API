from flask import Blueprint, request, jsonify
from ..utils.wishlist_utils import add_wishlist

add_wishlist_bp = Blueprint('add_wishlist', __name__)

@add_wishlist_bp.route('/add-wishlist', methods=['POST'])
def handle_add_wishlist():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        response = add_wishlist(data['name'], data['email'], data['discord_username'], data['reason'], data['how_learned'])
        return jsonify({"message": response}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing data for {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
