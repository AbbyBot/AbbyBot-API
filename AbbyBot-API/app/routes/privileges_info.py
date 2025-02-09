from flask import Blueprint, jsonify
from ..utils.privileges_info_utils import fetch_privileges_info

privileges_info_bp = Blueprint('privileges_info', __name__)

@privileges_info_bp.route('/privileges-info', methods=['GET'])
def privileges_info():
    response = fetch_privileges_info()
    return jsonify(response)