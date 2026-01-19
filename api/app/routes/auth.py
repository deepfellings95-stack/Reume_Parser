from flask import Blueprint, request, current_app, jsonify
from app.models.models import Users
from app.services.set_users import set_user
from flask_login import current_user, login_user, logout_user
from app.services.otp_service import request_otp, verify_otp
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
import os

load_dotenv()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        user = Users.query.filter_by(email = email).first()
        if not user.password:
            print('login  here')
            return jsonify({'success':False, 'message':"User not exists"}), 401
        
        try:
            print('login  here2')
            
            if user and check_password_hash(user.password, password):
                print('login  here3')
                
                login_user(user)
                return jsonify({'success':True, 'message':'valid id'}), 200
            else:
                print('login  here4')
                
                return jsonify({'success':False, 'message':'Wrong Password'}), 400
        except Exception as e:
            print('login  here5')
            
            return jsonify({'success':False,'message':f'error: {e}'}), 401
    except Exception as e:
        print('login  here6')
        
        return jsonify({'success':False,'message':f'error: {e}'}), 401
    
@auth_bp.route('/send_otp', methods=['GET','POST'])
def send_otp():
    if request.method == 'GET':
        return jsonify({'success':False, 'message':'This is GET method, donnot worry developers fault'})
    
    sender_email = os.getenv("BREVO_EMAIL2")
    if not sender_email or sender_email is None:
        return jsonify({'success':False, 'message':"sender_email is none"})
    try: 
        email = request.json
        extracted_email = email.get('email')
        
        success, message, status = request_otp(extracted_email)
        print(success)
        print(status)
        if status != 200:
            return jsonify({'success':success, 'message':message}), status
        return jsonify({'success':success, 'message':message}), status
    except Exception as e:
        return jsonify({'success':False,'message':f"error {e}"}), 400
        
@auth_bp.route('/verify_otp', methods=['GET','POST'])
def otp_verification():
    if request.method == 'GET':
        return jsonify({'success':False,'message':"internal server error"}), 400
        
    data = request.json
    extracted_email = data.get('email')
    extracted_otp = data.get('otp')
    
    if not extracted_email or not extracted_otp:
        return jsonify({'success':False, 'message':'Invalied OTP format, it should be a number'}), 400
        
    success, message, status = verify_otp(extracted_email, extracted_otp)
    
    if success:
        user_data = data.get('userData')
        isUserSet , msg, res = set_user(user_data)
        print(isUserSet)
        print(res)
        
        if isUserSet:
            return jsonify({'success':True, 'message':msg}), res
        return jsonify({'success':False, 'message':msg}), res
    print(message)    
    return jsonify({'success':False ,'message':message}), status
    
    
@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return 'Logged out', 200