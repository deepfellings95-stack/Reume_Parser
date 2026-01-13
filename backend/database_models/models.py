from database.database import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usage = db.Column(db.String)
    name = db.Column(db.String(250), nullable= False)
    google_name = db.Column(db.String(250))
    email = db.Column(db.String(100), unique = True)
    google_email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(250))
    dob = db.Column(db.DateTime())
    purpose = db.Column(db.String(250))
    google_id = db.Column(db.String(255), unique=True)
    auth_provider = db.Column(db.String(50))  # 'google', 'local'
    resumes = db.relationship('Resume', backref='user', lazy=True)
    details = db.relationship('UserDetails', backref='user', lazy=True , uselist=False)
    #resume_details = db.relationship('resumeDetails', backref='user', lazy=True, uselist=False)


    def set_password(self, password):
        self.password =  generate_password_hash(password)

    def get_password(sef, password):
        return check_password_hash(self.password, password)
