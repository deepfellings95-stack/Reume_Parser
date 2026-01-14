from flask import Blueprint, request, current_user, current_app
from app.models.models import Users



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET','POST'])
def signupUser():
    pass
        
    