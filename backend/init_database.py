from app import app
from database.database import db

print(db)
with app.app_context():
    db.drop_all()
    db.create_all()
