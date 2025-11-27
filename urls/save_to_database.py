from database.database import db
from database_models.posts import Post
from werkzeug.utils import secure_filename

class Save:
    def __init__(self, filename, text, user_id):
        self.filename = filename
        self.text = text
        self.user_id = user_id

    def save_text(self):
        try:
            new_post = Post(
                filename = secure_filename(self.filename),
                text = secure_filename(self.text),
                user_id = self.user_id
                )
            db.session.add(new_post)
            db.session.commit()
            return 'saved'
        except Exception as e:
            return f"error Occur {e}"
