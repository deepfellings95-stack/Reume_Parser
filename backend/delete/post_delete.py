from database.database import db
from database_models.posts import Post
from flask import Blueprint,  current_app, redirect, render_template, url_for

delete_bp = Blueprint('dl', __name__)

@delete_bp.route('/post_delete/<int:id>')
def deleting_process(id):
    post = Post.query.filter_by(id = id).first()
    post.is_deleted = True
    db.session.commit()
    return redirect(url_for('home'))
