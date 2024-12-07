from flask import Blueprint, jsonify, request
from ..utils.abbybot_commands_utils import (
    get_control_commands,
    get_image_commands,
    get_minigames_commands,
    get_music_commands, 
    get_utility_commands, 
    get_user_commands, 
    get_all_commands,
    get_categories
    )

abbybot_commands_bp = Blueprint('abbybot_commands', __name__)

@abbybot_commands_bp.route('/abbybot_commands', methods=['GET'])
def get_abbybot_commands():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_all_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/control', methods=['GET'])
def get_control_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_control_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/minigames', methods=['GET'])
def get_minigames_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_minigames_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/music', methods=['GET'])
def get_music_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_music_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/utility', methods=['GET'])
def get_utility_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_utility_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/user', methods=['GET'])
def get_user_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_user_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/image', methods=['GET'])
def get_image_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_image_commands(language_id)
    return jsonify(commands)

# Categories list route

@abbybot_commands_bp.route('/abbybot_commands/categories', methods=['GET'])
def get_categories_route():
    categories = get_categories()
    return jsonify(categories)