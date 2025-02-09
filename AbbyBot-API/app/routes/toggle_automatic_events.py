from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..utils.birthday_utils import toggle_birthday

toggle_automatic_events_bp = Blueprint('toggle_automatic_events', __name__)

@toggle_automatic_events_bp.route('/toggle_automatic_events', methods=['POST'])
@swag_from({
    'tags': ['AbbyBot Servers'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'guild_id': {
                        'type': 'string',
                        'description': 'The ID of the guild'
                    },
                    'activated_events': {
                        'type': 'integer',
                        'description': 'The new state of automatic events (0 or 1)'
                    }
                },
                'required': ['guild_id', 'activated_events']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Automatic events toggled successfully',
            'examples': {
                'application/json': {
                    'success': 'Activated auto events for guild {guild_id}',
                    'status_code': 200
                }
            }
        },
        400: {
            'description': 'Invalid input',
            'examples': {
                'application/json': {
                    'error': 'Invalid value for activated_events. It must be 0 or 1.',
                    'status_code': 400
                }
            }
        },
        404: {
            'description': 'No guild found with the provided guild_id',
            'examples': {
                'application/json': {
                    'error': 'No guild found with the provided guild_id',
                    'status_code': 404
                }
            }
        }
    }
})
def toggle_automatic_event():

    guild_id = request.json.get('guild_id')
    activated_events = request.json.get('activated_events')
    

    if not isinstance(activated_events, int):
        return jsonify({"error": "Invalid value for activated_events. It must be a number (0 or 1).", "status_code": 400}), 400
  
    

    if activated_events not in [0, 1]:
        return jsonify({"error": "Invalid value for activated_events. It must be 0 or 1.", "status_code": 400}), 400


    rows_affected = toggle_birthday(guild_id, activated_events)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the activated_events value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        if activated_events == 1:
            return jsonify({"success": f"Activated auto events for guild {guild_id}", "status_code": 200}), 200
        else:
            return jsonify({"success": f"Deactivated auto events for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404

