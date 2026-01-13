from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from database_models.models import User
from database_models.user_details import UserDetails
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session, current_app, render_template_string
from database.database import db
import uuid
from datetime import datetime
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from extensions import oauth


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST','GET'])
def signup_user():
    try:
        if request.method == 'POST':
            uid = session.get('uid')
                     
            new_user = User.query.filter_by(id = uid).first()

            name = request.form['name']
            print(name)
            usage = request.form['usage']

            password = request.form['password']

            dob = request.form['dob']

            purpose = request.form['purpose']

            new_user.usage = usage
            new_user.name = new_user.name
            new_user.email = new_user.email
            new_user.google_name = new_user.google_name
            new_user.google_email = new_user.google_email
            new_user.password = generate_password_hash(password)
            new_user.dob = datetime.strptime(dob, "%Y-%m-%d")
            new_user.purpose = purpose
            
            company_name = request.form.get('corporate_name')
            company_mail = request.form.get('corporate_mail')
            employee_count = request.form.get('strength')
            sector = request.form.get('sector')
            others = request.form.get('corporate_other')
            university_name = request.form.get('university_name')
            university_mail = request.form.get('university_mail')
            city = request.form.get('city')
            provine = request.form.get('provine')
            personal_number = request.form.get('personal_number')
            personal_city = request.form.get('personal_city')
            personal_state = request.form.get('state')

            db.session.add(new_user)
            db.session.commit()
            
            userdetails = UserDetails(
                user_id = new_user.id,
                company_name = company_name,
                company_mail = company_mail,
                employee_count = employee_count,
                sector = sector,
                others = others,
                university_name = university_name,
                university_mail = university_mail,
                city = city,
                provine = provine,
                personal_number = personal_number,
                personal_city = personal_city,
                personal_state = personal_state,
                
            )
            
            db.session.add(userdetails)
            db.session.commit()
            
            return redirect(url_for('auth.loginUser'))
        else:
            return render_template('signup.html', withoutGPT= True)
    except Exception as e:
        print(e)
        return f" An error Occur {e}"

@auth_bp.route('/signupOTP')
def signupotp():
    return render_template('signupOTP.html')
    
    
@auth_bp.route('/login', methods=['POST','GET'])
def loginUser():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            existing_user = User.query.filter_by(email = email).first()
            
            if not existing_user.password:
                html_content = """<p style="color:red">Password not set, <span> click on <a href="{{ url_for('otp.forget_password') }}">forget password</a> to set the password.</span></p>"""
                return render_template_string(html_content)
            print(existing_user.password)
            try: 
                if existing_user and check_password_hash(existing_user.password, password):
                    login_user(existing_user)
                    return redirect(url_for('home'))
                
                else:
                    return render_template('login.html', wp=True)
            except Exception as e: 
                print(e)
                return redirect(url_for('auth.signupotp'))
        else:
            return render_template('login.html')
    except Exception as e:
        html = """<p>may be you need to signin first if you see none type error. click on <a href="{{ url_for('auth.signupotp') }}">Signup</a>. Thank me later .</p>"""
        return render_template_string(html)
    

@auth_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/google/callback')
def google_callback():
    token = oauth.google.authorize_access_token()

    user_info = oauth.google.get(
        'https://www.googleapis.com/oauth2/v3/userinfo'
    ).json()

    google_email = user_info['email']
    google_id = user_info['sub']
    google_name = user_info.get('name')

    # Look for user by ANY email
    user = User.query.filter(
        (User.email == google_email) |
        (User.google_email == google_email)
    ).first()

    if not user:
        user = User(
            name=google_name,                 # ✅ FIX
            email=google_email,               # ✅ FIX
            google_name=google_name,           # ✅ FIX
            google_email=google_email,         # ✅ FIX
            google_id=google_id,
            auth_provider='google'
        )
        db.session.add(user)
        db.session.commit()
    
    uid = User.query.filter((User.email == google_email) |
        (User.google_email == google_email)).first()
        
    session['uid'] = uid.id
    session['name'] = google_name
    userdetails = UserDetails.query.filter_by(user_id = uid.id).first()
    if not userdetails:
        return redirect(url_for('auth.signup_user'))   
    return render_template('login.html', email = google_email)


    
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@auth_bp.route('/reset_password', methods=['GET','POST'])
def reset_password():
    if request.method =='GET':
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
    
    stored_email = session.get('otp_email')
    session.pop('otp_email')
    password = request.form.get('pass')
    user = User.query.filter_by(email = stored_email).first()
    if user:
        user.password = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.loginUser'))
    else:
        return redirect(url_for('auth.singup_user'))



