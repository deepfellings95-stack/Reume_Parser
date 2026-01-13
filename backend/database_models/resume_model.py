from database.database import db
from datetime import datetime

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)

    extracted_text = db.Column(db.Text)
    extracted_json = db.Column(db.JSON)

    ocr_engine = db.Column(db.String(20))  # TESSERACT / OCRSPACE
    status = db.Column(db.String(20), default="completed")  # processing / completed / failed
    is_deleted = db.Column(db.Boolean , default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
