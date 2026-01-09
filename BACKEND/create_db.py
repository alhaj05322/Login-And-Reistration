from app import create_app
from app.extensions import db
from app.models import Base


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(db.engine)
        print("Database & Tables Created")