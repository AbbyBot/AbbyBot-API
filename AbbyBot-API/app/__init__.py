from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://api.abbybotproject.com", "http://localhost:5000"],
                                 "methods": ["GET", "POST", "OPTIONS"],
                                 "allow_headers": ["Content-Type", "Authorization"]
                                }})

    from .routes.bot_info import bot_info_bp
    from .routes.user_info import user_info_bp
    from .routes.server_settings import server_settings_bp
    from .routes.photos import photos_bp
    from .routes.server_dashboard import server_dashboard_bp  
    from .routes.user_servers import user_servers_bp
    from .routes.update_birthday import update_birthday_bd
    from .routes.update_abbybot_theme import update_abbybot_theme_bd
    from .routes.update_language import update_language_bp
    from .routes.toggle_automatic_events import toggle_automatic_events_bp
    from .routes.toggle_logs import toggle_logs_bp
    from .routes.set_prefix import set_prefix_bp
    from .routes.set_birthday_channel import set_birthday_channel_bp
    from .routes.set_logs_channel import set_logs_channel_bp
    from .routes.privileges_info import privileges_info_bp
    from .routes.view_handler import view_handler_bp
    from .routes.abbybot_themes import abbybot_themes_bp
    from .routes.server_channels import server_channels_bp
    from .routes.update_channels import update_channel_bd

    app.register_blueprint(bot_info_bp)
    app.register_blueprint(user_info_bp)
    app.register_blueprint(server_settings_bp)
    app.register_blueprint(photos_bp)
    app.register_blueprint(server_dashboard_bp)
    app.register_blueprint(user_servers_bp)
    app.register_blueprint(update_birthday_bd)
    app.register_blueprint(update_abbybot_theme_bd)
    app.register_blueprint(update_language_bp)
    app.register_blueprint(toggle_automatic_events_bp)
    app.register_blueprint(toggle_logs_bp)
    app.register_blueprint(set_prefix_bp)
    app.register_blueprint(set_birthday_channel_bp)
    app.register_blueprint(set_logs_channel_bp)
    app.register_blueprint(privileges_info_bp)
    app.register_blueprint(view_handler_bp)
    app.register_blueprint(abbybot_themes_bp)
    app.register_blueprint(server_channels_bp)
    app.register_blueprint(update_channel_bd)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5002)
