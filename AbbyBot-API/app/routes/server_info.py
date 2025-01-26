from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from ..utils.server_info_utils import get_server_info
import json

load_dotenv()

server_info_bp = Blueprint('server_info', __name__)

@server_info_bp.route('/server-info', methods=['GET'])
def list_photos():
    guild_id = request.args.get('guild_id')
    if not guild_id:
        return jsonify({"error": "guild_id is required"}), 400

    server_info = get_server_info(guild_id)
    return jsonify(json.loads(server_info))
