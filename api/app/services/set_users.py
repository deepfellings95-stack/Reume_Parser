from app.extensions.database import db
from app.models.models import Users, UserDetails
from werkzeug.security import generate_password_hash , check_password_hash
from datetime import datetime

def set_user(data):
    
    if not data:
        return False, "No data Received"
        
    existing_user = Users.query.filter_by(email = data.get('email')).first()
    if existing_user:
        return False, "User Already exists"
        

        
    try:
        new_user = Users()
        new_userdetail = UserDetails()
          
        new_user.name = data.get('name') or ''
        new_user.email = data.get('email') or ''
        password = data.get('password')
        new_user.password = generate_password_hash(password) or ''
        new_user.username = data.get('username') or ''
        dob_str = data.get('dob')
        if dob_str:
            new_user.dob = datetime.strptime(dob_str, '%Y-%m-%d').date() or ''
            
        new_user.account_type = data.get('accountType') or ''
        
        db.session.add(new_user)
        db.session.flush()
    
    
        new_userdetail.userid = new_user.id or ''
        new_userdetail.city = data.get('city') or ''
        new_userdetail.state = data.get('state') or ''
        new_userdetail.zip_code = data.get('zipcode') or ''
        new_userdetail.planet = data.get('other_location') or ''
        new_user.university_name = data.get('universityName') or ''
        new_userdetail.course = data.get('course') or ''
        new_userdetail.student_id = data.get('student_id') or ''
        new_userdetail.university_link = data.get('university_link') or ''
        new_userdetail.need = data.get('need') or ''
        new_userdetail.company_name = data.get('company_name') or ''
        new_userdetail.company_type = data.get('company_type') or ''
        new_userdetail.company_strength = data.get('company_strength') or ''
        new_userdetail.company_web_link = data.get('company_web_link') or ''
        new_userdetail.job_title = data.get('job_title') or ''
        new_userdetail.age = data.get('age') or ''
        new_userdetail.need = data.get('need') or ''
        new_userdetail.members = data.get('members') or ''
        new_userdetail.education = data.get('education') or ''
        
        db.session.add(new_userdetail)
        db.session.commit()
        
        return True, "stored", 201
        
    except Exception as e:
        db.session.rollback()
        return False, f'Error : {e}'
    
