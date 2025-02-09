from flask import Blueprint, jsonify, request
from flasgger import swag_from
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
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of all commands',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'command': {'type': 'string'},
                        'description': {'type': 'string'},
                        'usage': {'type': 'string'}
                    }
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'language_id',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Language ID for the commands'
        }
    ]
})
def get_abbybot_commands():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_all_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/control', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of control commands',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'command': {'type': 'string'},
                        'description': {'type': 'string'},
                        'usage': {'type': 'string'}
                    }
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'language_id',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Language ID for the commands'
        }
    ]
})
def get_control_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_control_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/minigames', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of minigames commands',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'command': {'type': 'string'},
                        'description': {'type': 'string'},
                        'usage': {'type': 'string'}
                    }
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'language_id',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Language ID for the commands'
        }
    ]
})
def get_minigames_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_minigames_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/music', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of music commands',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'command': {'type': 'string'},
                        'description': {'type': 'string'},
                        'usage': {'type': 'string'}
                    }
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'language_id',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Language ID for the commands'
        }
    ]
})
def get_music_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_music_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/utility', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of utility commands',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'command': {'type': 'string'},
                        'description': {'type': 'string'},
                        'usage': {'type': 'string'}
                    }
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'language_id',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Language ID for the commands'
        }
    ]
})
def get_utility_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_utility_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/user', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of user commands',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'command': {'type': 'string'},
                        'description': {'type': 'string'},
                        'usage': {'type': 'string'}
                    }
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'language_id',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Language ID for the commands'
        }
    ]
})
def get_user_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_user_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/image', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of image commands',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'command': {'type': 'string'},
                        'description': {'type': 'string'},
                        'usage': {'type': 'string'}
                    }
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'language_id',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Language ID for the commands'
        }
    ]
})
def get_image_commands_route():
    language_id = request.args.get('language_id', default=1, type=int)
    commands = get_image_commands(language_id)
    return jsonify(commands)

@abbybot_commands_bp.route('/abbybot_commands/categories', methods=['GET'])
@swag_from({
    'tags': ['AbbyBot Commands'],
    'responses': {
        200: {
            'description': 'List of command categories',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'category_name': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_categories_route():
    categories = get_categories()
    return jsonify(categories)