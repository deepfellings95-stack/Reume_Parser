import random
import datetime
import requests
import os
from database_models.models import User
from database.database import db
from database_models.user_details import UserDetails
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from extension.redis_client import redis_client
from security.otp_service import (
    generate_otp, save_otp, redis_verify_otp, can_resend
)


# Assuming you have a db instance
# db = SQLAlchemy()

otp_bp = Blueprint('otp', __name__)

def send_email_brevo(to_email, otp):
    """Sends OTP using Brevo API"""
    api_key = os.getenv('BREVO_API_KEY')
    url = os.getenv('BREVO_URL')
    
    # IMPORTANT: The sender email MUST be verified in your Brevo Dashboard
    # Go to: Brevo -> Senders & IP -> Senders -> Add a sender
    sender_email = os.getenv('BREVO_EMAIL') 
    
    payload = {
        "sender": {"name": "Resume Parser", "email": sender_email},
        "to": [{"email": to_email}],
        "subject": "Your Verification Code",
        "htmlContent": f"<html><body><h1>Your OTP is: {otp}</h1><p>It will expire in 5 minutes.</p></body></html>"
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Brevo Status: {response.status_code}")
        if response.status_code != 201:
            print(f"Brevo Error: {response.text}") # This will show the exact error
        return response.status_code == 201
    except Exception as e:
        print(f"Request Error: {e}")
        return False

@otp_bp.route('/request_otp', methods=['POST'])
def request_otp():
    email = request.form.get('email')
    user = User.query.filter_by(email = email).first()
    if user:
        return render_template('login.html', exists=True)
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    otp = generate_otp()
    save_otp(redis_client, email, otp)

    success = send_email_brevo(email, otp)
    session['email'] = email

    if success:
        print(f'OTP sent successfully!{otp}')
        return render_template('signupOTP.html', otp_received=True, mail = email)
    else:
        return jsonify({
            "error": "Failed to send OTP email. Please try again later."
        }), 500
        
@otp_bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'GET':
        html_content = '''{% extends "base.html" %}{% block title %}Recover Email{% endblock %}{% block content %}
        <div class="max-h-screen my-auto flex justify-center items-center">
	<div class="neu-card max-w-md w-full p-8">
		<h2 class="text-3xl font-bold text-center mb-6 text-gray-700">
		Recover Email
		</h2>
		<form id="oauthForm" action="/forget_password" method="POST" class="space-y-5">
        <fieldset id="base_data" class="space-y-5"> 
        					<input type='email'  name="email" placeholder="yourmail@mail.com" class="neu-input" required>
					<button type="submit" class="neu-btn w-full mt-2 text-gray-700">Get OTP</button>
                    			</fieldset>

		</form>
        		<p class="text-center text-gray-600 mt-4 text-sm">
		{% if 'signup' in request.path %}
		Already have an account? <a href="/auth/login" class="text-blue-500 font-medium">Login</a><br>
		<a href="{{ url_for('auth.google_login') }}" class="text-blue-500 font-medium">Signup using Google <i class="fa fa-google" style="font-size:16px"></i></a>

		{% endif %}
		</p>
	</div>
</div>{% endblock %}'''
        return render_template_string(html_content)
    email = request.form.get('email')
    print(email)
    
    otp = generate_otp()
    save_otp(redis_client, email, otp)

    success = send_email_brevo(email, otp)
    session['email'] = email
    print(f'emais is q:{email}')

    if success:
        print('OTP sent successfully!')
        return render_template('signupOTP.html', otp_received=True)
    else:
        return jsonify({
            "error": "Failed to send OTP email. Please try again later."
        }), 500



@otp_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    try:
        email = session.get('email')
        print(email)
        user_otp = request.form.get('otp')
        
        success, message = redis_verify_otp(redis_client, email, user_otp)

        if not success:
            return jsonify({"error": message}), 400

        user = User.query.filter_by(email = email).first()

        if not user:
            new_user= User(
                email = email,
                name = 'unknown'
            )
            db.session.add(new_user)
            db.session.commit()
            uid = User.query.filter_by(email = email).first()
        
            session['uid'] = uid.id
            return redirect(url_for('auth.signup_user'))
        print(user.email)
        us_details = UserDetails.query.filter_by(user_id = user.id).first()
        if us_details:
            html_content = '''{% extends "base.html" %}{% block title %}Set Password{% endblock %}{% block content %}
        <div class="max-h-screen my-auto flex justify-center items-center">
    <div class="neu-card max-w-md w-full p-8">
        <h2 class="text-3xl font-bold text-center mb-6 text-gray-700">
        password
        </h2>
        <form id="oauthForm" action="{{ url_for('auth.reset_password') }}" method="POST" class="space-y-5">
        <fieldset id="base_data" class="space-y-5"> 
                            <input id='pass' type='password'  name="pass" placeholder="Ener New Password" class="neu-input" required>
                            <input id='confpass' type='password'  name="confirmPass" placeholder="Confirm New Password" class="neu-input" required>
                    <button type="submit" class="neu-btn w-full mt-2 text-gray-700">Submit</button>
                                </fieldset>

        </form>
                <p class="text-center text-gray-600 mt-4 text-sm">
        {% if 'signup' in request.path %}
        Already have an account? <a href="/auth/login" class="text-blue-500 font-medium">Login</a><br>
        <a href="{{ url_for('auth.google_login') }}" class="text-blue-500 font-medium">Signup using Google <i class="fa fa-google" style="font-size:16px"></i></a>

        {% endif %}
        </p>
    </div>
    </div>
    <script>
    const password = document.getElementById('pass');
    const confirmPassword = document.getElementById('confpass');

    form.addEventListener('submit', function (event) {
      if (password.value !== confirmPassword.value) {
          errorMsg.classList.remove("hidden");
          event.preventDefault(); // Stop form submit
      }
      else if(baseData.style.display !== 'none'){
          event.preventDefault();
      } else {
          errorMsg.classList.add("hidden");
      }
    });

    </script>
    {% endblock %}'''
            return render_template_string(html_content)
        else:
            return redirect(url_for('auth.signup_user'))
                
        
            
        
        # OTP is correct! 
        # Here you would create the user in your database
        # user = User(email=stored_email, ...)
        # db.session.add(user)
        # db.session.commit()
        
        # Clear session
    
    except Exception as e:
        return jsonify({"error": f"Invalid OTP{e}"}), 400
