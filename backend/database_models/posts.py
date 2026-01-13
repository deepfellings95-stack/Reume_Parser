from database.database import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Post(db.Model):
    __tablename__ = 'text'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(400))
    filepath = db.Column(db.String(400))
    text = db.Column(db.Text)
    resume_json = db.Column(db.JSON)
    ocr_engine = db.Column(db.String())
    status = db.Column(db.String())
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(), default = datetime.utcnow)
    
    resumeDetails = db.relationship('ResumeDetails', backref='text', lazy=True, uselist = False)
    

    user_id = db.Column(UUID(as_uuid = True), db.ForeignKey('user.id'), nullable=False)
