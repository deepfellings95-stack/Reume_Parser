from database.database import db
from database_models.posts import Post
from database_models.resume_model import Resume
from werkzeug.utils import secure_filename
from flask_login import current_user
import uuid

class Save:


    def __init__(self, filename, text, user_id):
    

        self.filename = filename
        self.filepath = filepath
        self.text = text
        self.json = json
        self.ocr_engine = ocr_engine
        self.status = status
        self.user_id = user_id

    def save_text(self):
        try:
            new_post = Post(
                filename = secure_filename(self.filename),
                filepath = self.filepath,
                text = self.text,
                json = self.json,
                ocr_engine = self.ocr_engine,
                status = self.status,
                user_id = self.user_id
                )
            db.session.add(new_post)
            db.session.commit()
            return 'saved'
        except Exception as e:
            return f"error Occur {e}"
