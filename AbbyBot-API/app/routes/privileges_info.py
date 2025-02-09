from flask import Blueprint, jsonify
from flasgger import swag_from
from ..utils.privileges_info_utils import fetch_privileges_info

privileges_info_bp = Blueprint('privileges_info', __name__)

@privileges_info_bp.route('/privileges-info', methods=['GET'])
@swag_from({
    'tags': ['AbbyBotProject Website'],
    'responses': {
        200: {
            'description': 'A list of privileges information',
            'schema': {
                'type': 'object',
                'properties': {
                    'privileges': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'privilege_name': {'type': 'string'},
                                'value': {'type': 'integer'},
                                'rol_meaning': {'type': 'string'},
                                'how_to_get': {'type': 'string'},
                                'xp_multiplier': {'type': 'number'},
                                'exclusive_access': {'type': 'boolean'}
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'No privileges information found'
        }
    }
})
def privileges_info():
    response = fetch_privileges_info()
    return jsonify(response)