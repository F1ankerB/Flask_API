from flask_migrate import Migrate
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        migrate = Migrate(app, db)
        from app.models.user import User
        db.create_all()
        print("Database tables created successfully!")
