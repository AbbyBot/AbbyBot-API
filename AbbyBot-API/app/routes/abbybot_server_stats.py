from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.abbybot_server_stats_utils import get_all_server_stats, get_all_privileges

abbybot_server_stats_bp = Blueprint('abbybot_server_stats', __name__)

@abbybot_server_stats_bp.route('/server_stats', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Servers'],
    'responses': {
        200: {
            'description': 'A list of server stats',
            'examples': {
                'application/json': [
                    {
                        "servers_using_abbybot": 120,
                        "users_served": 120000,
                        "xp_earned": 1000000
                    }
                ]
            }
        }
    }
})
def get_server_stats():
    stats = get_all_server_stats()
    return jsonify(stats)
