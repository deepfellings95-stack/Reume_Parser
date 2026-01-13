from flask import Flask, redirect, render_template, request, current_app, url_for
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from urls.routes import upload_bp
from config import Config
from database.database import db
from auth.routes import auth_bp
from database_models.models import User
from database_models.posts import Post
from flask_login import login_required, current_user
from flask_migrate import Migrate
import os
import sys
import subprocess
from delete.post_delete import delete_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

            
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(upload_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(auth_bp, url_prefix = '/auth')


@app.route('/', methods=['POST','GET'])
def home():
    posts = ''
    try:
        if current_user.is_authenticated:
            posts = Post.query.filter_by(user_id = current_user.id).all()
            if request.method == "GET":
                return render_template('home.html', posts=posts)

    except Exception as e:
        return f" An Error Occur {e}"

    if request.method =='GET':
        return render_template('home.html')
    
    try:
        file = request.files.get('file')

        if not file or file.filename == '':
            return "No file uploaded"

        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)      # FIXED

        ext = filename.rsplit('.', 1)[1].lower()
        image_ext = ['jpeg', 'jpg', 'png']

        if ext == "pdf":
            return redirect(url_for('urls.parsing_pdf', filename=filename))
        elif ext == "docx":
            return redirect(url_for('urls.parsing_documnets', filename=filename))
        elif ext in image_ext:
            return redirect(url_for('urls.parsing_image', filename = filename))
        elif ext == 'txt':
            return redirect(url_for('urls.parsing_text', filename = filename))
        else:
            return f"Invalied File: {filename}"

    except Exception as e:
        return str(e)   # FIXED for debugging




if __name__ == '__main__':   # FIXED
    app.run(debug=True)
