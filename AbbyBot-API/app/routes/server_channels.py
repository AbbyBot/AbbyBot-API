from flask import Blueprint, request, jsonify
from ..utils.db import get_db_connection

server_channels_bp = Blueprint('server_channels', __name__)

@server_channels_bp.route('/server-channels', methods=['GET'])
def get_server_dashboard():
    guild_id = request.args.get('guild_id')

    if not guild_id:
        return jsonify({'error': 'Missing required parameter: guild_id'}), 400
    
    conn = get_db_connection("AbbyBot_Rei")
    
    try:
        with conn.cursor() as cursor:
            query = """
                    SELECT
                      id, guild_id, channel_id, channel_title 
                    FROM
                      server_channels 
                    WHERE
                      guild_id = %s;
                    """
            cursor.execute(query, (guild_id,))
            result = cursor.fetchall()

            channel_list = []
            for row in result:
                channel_data = {
                    'id': row[0],
                    'guild_id': row[1],
                    'channel_id': row[2],
                    'channel_title': row[3]
                }
                channel_list.append(channel_data)

            return jsonify(channel_list)

    finally:
        conn.close()
