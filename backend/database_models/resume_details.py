from database.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ResumeDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    raw_json = db.Column(db.JSON)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String())
    phone = db.Column(db.String())
    skillset = db.Column(db.JSON)
    education = db.Column(db.JSON)
    experience = db.Column(db.JSON)
    status = db.Column(db.String())
    
    extracted_text_id = db.Column(db.Integer, db.ForeignKey('text.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid = True), db.ForeignKey('user.id'), nullable=False)