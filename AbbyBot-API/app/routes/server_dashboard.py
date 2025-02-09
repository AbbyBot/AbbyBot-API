from flask import Blueprint, request, jsonify
from ..utils.server_dashboard_utils import fetch_server_dashboard

server_dashboard_bp = Blueprint('server_dashboard', __name__)

@server_dashboard_bp.route('/server-dashboard', methods=['GET'])
def get_server_dashboard():
    guild_id = request.args.get('guild_id')
    page = request.args.get('page', 1)
    limit = 10

    if not guild_id:
        return jsonify({'error': 'Missing required parameter: guild_id'}), 400

    response_object = fetch_server_dashboard(guild_id, page, limit)
    return jsonify(response_object), 200
