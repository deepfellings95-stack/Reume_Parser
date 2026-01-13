from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OpenRouter_API_KEY = os.getenv('OPENRouter_CHATGPT_KEY2')
    OCRSpace_API_KEY = os.getenv('OCRSpace_API_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt") 
    UPLOAD_FOLDER = 'upload'
    CONVERT_FOLDER = 'upload/convert'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET  = os.getenv("GOOGLE_CLIENT_SECRET")

    
