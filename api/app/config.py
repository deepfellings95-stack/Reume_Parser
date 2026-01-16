import os
from pathlib import Path
from app.extensions.database import db

class BaseConfig:
    BASE_DIR = Path(__file__).parent
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///db.sqlite3")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "uploads"
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY',"fdkjhkfghirdfe435jkh")
    
class DevConfig(BaseConfig):
    
    DEBUG=True

class ProdConfig(BaseConfig):
    DEBUG = False
    
config = {'development': DevConfig,
'production':ProdConfig}