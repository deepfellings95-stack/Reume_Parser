from app.extensions.database import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from datetime import DateTime

class Users(db.Model, db.UserMixin):
    id = db.Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4, nullable=False)
    username = db.Column(db.String(250))
    name = db.Column(db.String(250))
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250))
    dob = db.Column(db.DateTime())
    
    