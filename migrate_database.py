from app import app
from database.database import db
from flask_migrate import upgrade, Migrate

migrate = Migrate(app, db)

with app.app_context():
    upgrade()  # applies all migrations
    print("Database migrated successfully!")
