from flask import Blueprint, render_template

view_handler_bp = Blueprint('view_handler', __name__)

@view_handler_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@view_handler_bp.app_errorhandler(400)
def bad_request_error(error):
    return render_template('400.html'), 400

@view_handler_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@view_handler_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@view_handler_bp.app_errorhandler(405)
def method_not_allowed_error(error):
    return render_template('405.html'), 405

@view_handler_bp.app_errorhandler(415)
def unsupported_media_type_error(error):
    return render_template('415.html'), 415