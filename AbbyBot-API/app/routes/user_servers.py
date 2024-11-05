from flask import Blueprint, jsonify, request
from ..utils.db import get_user_server_data
from ..utils.user_info_utils import get_user_info

user_servers_bp = Blueprint('user_servers', __name__)

@user_servers_bp.route('/user-servers', methods=['GET'])
def user_servers():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    user_data = get_user_server_data(user_id)
    user_info = get_user_info(user_id)

    if user_data and user_info:
        return jsonify({
            "user_id": user_id,
            "servers": user_data
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404
