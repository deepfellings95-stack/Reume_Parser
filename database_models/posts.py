from database.database import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(400))
    text = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
