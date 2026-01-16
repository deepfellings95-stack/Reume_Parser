from flask import Flask, jsonify, request
from flask_login import current_user, LoginManager, login_required
from flask_cors import CORS
import os
from app.extensions.database import db
from app.models.models import Users
from flask_login import login_required
import uuid
from flask_migrate import Migrate
from pathlib import Path
from app.config import config
from app.routes.auth import auth_bp


def create_app(config_name=None):
    app = Flask(__name__)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    
    upload_folder = Path(app.instance_path)/"uploads"
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    
    
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173"]
    )
    
    if config_name is None:
        config_name = os.getenv('CONFIG_NAME','development')
        
    app.config.from_object(config[config_name])
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    

    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return Users.query.get(uuid.UUID(user_id)).first()
        except Exception as e:
            return None

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({
            "success": False,
            "message": "User is not authenticated"
        }), 401
    @app.route('/api', methods=['GET','POST'])
    @login_required
    def home():       
        return jsonify({"status": True, "message": current_user.id})
    
    return app
    