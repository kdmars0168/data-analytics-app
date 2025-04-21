from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    demo_user = User.query.filter_by(email="demo@example.com").first()
    if demo_user is None:
        user = User(name="Demo User", email="demo@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        print("Demo user created successfully.")
    else:
        print("Demo user already exists.")
