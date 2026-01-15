from app.services.redis_services import generate_otp, save_otp, redis_verify_otp, can_resend
from flask import Blueprint, jsonify
from app.models.models import Users
from app.extensions.redis import redis_client
import requests
import os
from dotenv import load_dotenv

load_dotenv()
otp_bp = Blueprint('otp',__name__)

def send_email_brevo(email, otp):
    api_key = os.getenv('BREVO_API_KEY')
    brevo_url = os.getenv('BREVO_URL')
    
    sender_email = os.getenv('BREVO_EMAIL2')
    payload = {
        "sender": {"name": "Resume Parser", "email": sender_email},
        "to": [{"email": email}],
        "subject": "Your Verification Code",
        "htmlContent": f"<html><body><h1>Your OTP is: {otp}</h1><p>It will expire in 5 minutes.</p></body></html>"
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
        }
        
    try: 
        response = requests.post(brevo_url, json=payload, headers = headers)
        print(f"Brevo response: {response.status_code}")
        if response.status_code != 201:
            print(f"Brevo Error: {response.text}") # This will show the exact error
        return response.status_code == 201
    except Exception as e:
        print(f"Request Error: {e}")
        return False
    
def request_otp(email):
    if not email:
        return jsonify({'success':False, 'message':"email does not exist"}), 400
        
    user = Users.query.filter_by(email = email).first()
    if user:
        return jsonify({"success":False, 'message':"User already exist, did you forget password"}), 409
    
    otp = generate_otp()
    save_otp(redis_client, email, otp)
    
    success = send_email_brevo(email, otp)
    
    if success:
        return jsonify({'success': True, 'message':"OTP sent to email"}), 200
       
       
    else: 
        return jsonify({'success':False, 'message':'Failed to send Otp, internal server error'}), 500
    