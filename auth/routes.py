from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from database_models.models import User
from flask import Blueprint, request, render_template, redirect, url_for
from database.database import db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST','GET'])
def signup_user():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            existing_user = User.query.filter_by(email= email).first()
            if existing_user:
                return redirect(url_for('auth.loginUser'))

            new_user = User(
                name = name,
                email= email,
                password = generate_password_hash(password)
                )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.loginUser'))
        else:
            return render_template('signup.html')
    except Exception as e:
        return f" An error Occur {e}"

@auth_bp.route('/login', methods=['POST','GET'])
def loginUser():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            existing_user = User.query.filter_by(email = email).first()

            if existing_user and check_password_hash(existing_user.password, password):
                login_user(existing_user)
                return redirect(url_for('home'))
            elif not existing_user:
                return redirect(url_for('auth.signup_user'))
            
            else:
                return render_template('login.html', wp=True)
        else:
            return render_template('login.html')
    except Exception as e:
        return f"error occur {e}"
    

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))




































        
