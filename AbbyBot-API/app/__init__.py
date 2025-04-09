from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/*": {"origins": "*",  # Allow all origins
                                 "methods": ["GET", "POST", "OPTIONS"],
                                 "allow_headers": ["Content-Type", "Authorization"]
                                }})
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,  
                "model_filter": lambda tag: True, 
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }

    Swagger(app, config=swagger_config)

    @app.route('/')
    def index():
        return render_template('index.html')

    from .routes.bot_info import bot_info_bp
    from .routes.user_info import user_info_bp
    from .routes.server_settings import server_settings_bp
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
    from .routes.add_wishlist_user import add_wishlist_bp
    from .routes.api_status import status_bp
    from .routes.abbybot_commands import abbybot_commands_bp
    from .routes.abbybot_server_stats import abbybot_server_stats_bp
    from .routes.server_info import server_info_bp

    app.register_blueprint(bot_info_bp)
    app.register_blueprint(user_info_bp)
    app.register_blueprint(server_settings_bp)
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
    app.register_blueprint(add_wishlist_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(abbybot_commands_bp)
    app.register_blueprint(abbybot_server_stats_bp)
    app.register_blueprint(server_info_bp)

    return app
