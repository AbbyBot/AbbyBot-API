from flask import Blueprint, request, jsonify
from ..utils.db import get_db_connection
from ..utils.server_channels_utils import fetch_server_channels, NoChannelsFoundError

server_channels_bp = Blueprint('server_channels', __name__)

@server_channels_bp.route('/server-channels', methods=['GET'])
def get_server_dashboard():
    guild_id = request.args.get('guild_id')

    if not guild_id:
        return jsonify({'error': 'Missing required parameter: guild_id'}), 400
    
    if not guild_id.isdigit():
        return jsonify({'error': 'Invalid guild_id format'}), 400
    
    try:
        channel_list = fetch_server_channels(guild_id)
    except NoChannelsFoundError as e:
        return jsonify({'error': str(e)}), 404
    
    return jsonify(channel_list)
