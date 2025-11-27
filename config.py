from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OpenRouter_API_KEY = os.getenv('OPENRouter_CHATGPT_KEY')
    OCRSpace_API_KEY = os.getenv('OCRSpace_API_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '777'
    UPLOAD_FOLDER = 'upload'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
