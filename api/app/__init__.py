from flask import Flask, jsonify, request
from flask_login import current_user, LoginManager, login_required
from flask_cors import CORS
import os
from app.extensions.database import db
from flask_migrate import Migrate
from pathlib import Path
from app.config import config


def create_app(config_name=None):
    app = Flask(__name__)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    
    upload_folder = Path(app.instance_path)/"uploads"
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    
    
    CORS(app)
    
    if config_name is None:
        config_name = os.getenv('CONFIG_NAME','development')
        
    app.config.from_object(config[config_name])
    

    
    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    

    
    @login_manager.user_loader
    def load_user():
        pass

    
    @app.route('/api', methods=['GET','POST'])
    def home():
        
        try:
            if current_user.is_authenticated:
                return jsonify({'status':"success","message":"User is authenticated"})
            else:
                return jsonify({'status':"success","message":"User is Not authenticated"})
        except Exception as err:        
            return jsonify({"status": "success", "message": f"There is error {err}"})
    
    return app
    