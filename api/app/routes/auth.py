from flask import Blueprint, request, current_app, jsonify
from app.models.models import Users
from flask_login import current_user
from app.services.otp_service import request_otp
from dotenv import load_dotenv
import os

load_dotenv()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET','POST'])
def signupUser():
    pass
        

@auth_bp.route('/send_otp', methods=['GET','POST'])
def send_otp():
    if request.method == 'GET':
        return jsonify({'success':False, 'message':'This is GET method, donnot worry developers fault'})
    
    sender_email = os.getenv("BREVO_EMAIL2")
    if not sender_email or sender_email is None:
        return "sender_email is none"
    try: 
        email = request.json
        extracted_email = email.get('email')
        
        success, status = request_otp(extracted_email)
        print(success)
        print(status)
        if status != 200:
            return jsonify({'success':False, 'message':"Internal Error"}), 500
        return jsonify({'success':True, 'message':"we dit it"}), 200
    except Exception as e:
        return jsonify({'success':False,'message':f"error {e}"})