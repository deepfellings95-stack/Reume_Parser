from flask import Flask, redirect, render_template, request, current_app, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from urls.routes import upload_bp
from urls.resume_api import resume_api_bp
from config import Config
from database.database import db
from auth.routes import auth_bp
from database_models.models import User
from database_models.posts import Post
from flask_login import login_required, current_user
from flask_migrate import Migrate
from database_models.resume_model import Resume
from database_models.user_details import UserDetails
from database_models.resume_details import ResumeDetails
import os
import sys
import subprocess
from delete.post_delete import delete_bp
from flask_jwt_extended import JWTManager
from sqlalchemy.dialects.postgresql import UUID
import uuid
from extensions import oauth
from utils.otp_implementation import otp_bp
# from security.csrf import validate_csrf
# from security.csrf import generate_csrf_token


app = Flask(__name__)
app.config.from_object(Config)



# @app.before_request
# def csrf_protect():
    # validate_csrf()



# @app.context_processor
# def inject_csrf():
    # return dict(csrf_token=generate_csrf_token())

from flask_cors import CORS

CORS(
    app,
    supports_credentials=True,
    origins=[os.getenv('CORS_ORIGIN')]
)

oauth.init_app(app)
oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False  # dev only
)


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)
migrate = Migrate(app, db)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


            
login_manager = LoginManager()
login_manager.init_app(app)


app.register_blueprint(upload_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(auth_bp, url_prefix = '/auth')
app.register_blueprint(resume_api_bp, url_prefix = '/resume')
app.register_blueprint(otp_bp)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(uuid.UUID(user_id))
    except Exception as e:
        return None


@app.route('/', methods=['POST','GET'])
def home():
    posts = ''
    try:
        if current_user.is_authenticated:
            posts = Post.query.filter_by(user_id =current_user.id, is_deleted = False).all()
            if request.method == "GET":
                return render_template('home.html', posts=posts)

    except Exception as e:
        print(f'app error {e}')
        return f" An Error Occur is {e}"
    
    return render_template('home.html')


@app.route('/admin')
def admin():
    user = User.query.all()
    userdetails = UserDetails.query.all()
    post = Post.query.all()
    resumedetails = ResumeDetails.query.all()
    return render_template('admin.html', userdetails = userdetails , user = user, post = post, resumedetails = resumedetails)

#################################################################API############################################################

@app.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard_api():
    posts = Post.query.filter_by(
        user_id=current_user.id,
        is_deleted=False
    ).all()

    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "filename": post.filename,
            "text": post.text[:50],
            "status": post.status
        })

    return jsonify({
        "user": {
            "name": current_user.name or current_user.gmail_name
        },
        "posts": data
    })
    

if __name__ == '__main__':   # FIXED
    app.run(debug=True)
