from flask import Blueprint, render_template

view_handler_bp = Blueprint('view_handler', __name__)

@view_handler_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error_handler.html', error_code=404, error_message="Page Not Found"), 404

@view_handler_bp.app_errorhandler(400)
def bad_request_error(error):
    return render_template('error_handler.html', error_code=400, error_message="Bad Request"), 400

@view_handler_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('error_handler.html', error_code=403, error_message="Forbidden"), 403

@view_handler_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('error_handler.html', error_code=500, error_message="Internal Server Error"), 500

@view_handler_bp.app_errorhandler(405)
def method_not_allowed_error(error):
    return render_template('error_handler.html', error_code=405, error_message="Method Not Allowed"), 405

@view_handler_bp.app_errorhandler(415)
def unsupported_media_type_error(error):
    return render_template('error_handler.html', error_code=415, error_message="Unsupported Media Type"), 415

@view_handler_bp.app_errorhandler(418)
def teapot_error(error):
    return render_template('error_handler.html', error_code=418, error_message="I'm a teapot"), 418