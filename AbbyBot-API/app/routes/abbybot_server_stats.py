from flask import Blueprint, jsonify, request
from ..utils.abbybot_server_stats_utils import get_all_server_stats, get_all_privileges

abbybot_server_stats_bp = Blueprint('abbybot_server_stats', __name__)

@abbybot_server_stats_bp.route('/server_stats', methods=['GET'])
def get_server_stats():
    stats = get_all_server_stats()
    return jsonify(stats)

@abbybot_server_stats_bp.route('/privileges', methods=['GET'])
def get_privileges():
    privileges = get_all_privileges()
    return jsonify(privileges)
