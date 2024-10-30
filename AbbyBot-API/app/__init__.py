from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

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

    app.register_blueprint(bot_info_bp)
    app.register_blueprint(user_info_bp)
    app.register_blueprint(server_settings_bp)
    app.register_blueprint(photos_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5002)
