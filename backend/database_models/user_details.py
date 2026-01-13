from database.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class UserDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(UUID(as_uuid = True), db.ForeignKey('user.id'))
    company_name = db.Column(db.String(300), nullable = True)
    company_mail = db.Column(db.String(), nullable = True)
    employee_count = db.Column(db.Integer())
    sector = db.Column(db.String(250),nullable = True)
    others = db.Column(db.String())
    university_name = db.Column(db.String(300), nullable = True)
    university_mail = db.Column(db.String(), nullable = True)
    city = db.Column(db.String(250),nullable = True)
    provine = db.Column(db.String(250),nullable = True)
    personal_number = db.Column(db.Integer())
    personal_city = db.Column(db.String(50))
    personal_state = db.Column(db.String(50))