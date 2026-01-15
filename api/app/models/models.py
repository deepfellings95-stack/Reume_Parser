from app.extensions.database import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4, nullable=False)
    username = db.Column(db.String(250))
    name = db.Column(db.String(250))
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250))
    dob = db.Column(db.DateTime())
    account_type = db.Column(db.String())
    userDetails = db.relationship('UserDetails', backref="user", lazy=True)


class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    userid = db.Column(UUID(as_uuid = True), db.ForeignKey('user.id'), nullable=False)
    # common
    city = db.Column(db.String())
    state = db.Column(db.String())
    zip_code = db.Column(db.Integer())
    planet = db.Column(db.String())
    
    #Student data
    university_name = db.Column(db.String())
    course = db.Column(db.String())
    student_id = db.Column(db.String())
    university_link = db.Column(db.String())
    need = db.Column(db.String())
    
    #Corporate Data
    company_name = db.Column(db.String())
    company_type = db.Column(db.String())
    company_strength = db.Column(db.Integer())
    company_web_link = db.Column(db.String())
    job_title = db.Column(db.String())
    
    #personal Data
    age = db.Column(db.Integer())
    need = db.Column(db.String())
    members = db.Column(db.String())
    education = db.Column(db.String())