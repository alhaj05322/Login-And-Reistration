from flask import Blueprint, request, flash
from .models import User
from .extensions import db, login_manager
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import re

bp = Blueprint("main", __name__)

#endpoint for handling login
@bp.post("/login")
def login():
    if request.method == "POST":
        data = request.get_json()

        email = (data.get("email") or "").strip()
        password = data.get("password") or ""

        if not email:
            return {"message": "Email is required"}
        
        if not password:
            return {"message": "Password is required"}
        
        #Get the user from the database
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        if not user or not check_password_hash(user.password, password):
            return {"message": f"Invalid email or password {email}"}
        else:
            login_user(user)
            return {"message": f"User {user.name} logged in"}

@login_manager.user_loader
def load_user(user_id):
    # Return the User object corresponding to the user ID
    return db.get_or_404(User, user_id)

#endpoint for handling resgistraion
@bp.post("/register")
def register():
    
    if request.method == "POST":
        data = request.get_json()
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        password = data.get("password") or ""
        confirm = data.get("confirm") or ""
       
        #Set username to be between 3 to 80 chars
        if not (3 <= len(name) <= 80):
            return {"message": "User name must be between 3 and 80 chars"}

        #Check if user entered a valid email
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return {"message": "Invalid email"}
        #Check if user entered a valid passord
        if len(password) < 6:
            return {"message": "Passord need to be atleast 6 chars"}

        #Check if passord and confirm passord are matched
        if password != confirm:
            return {"message": "Passowrd do not match"}

        #If data is valid ad user to the database
        try:
            pass_hash = generate_password_hash(password)
            user = User(name=name, email=email, password=pass_hash)
            db.session.add(user)
            db.session.commit()
            return {"message": f"user {name} is added to the database"}
        except IntegrityError:
            db.session.rollback()
            return {"message": "Username or email is already registered"}
@bp.post("/logout")
@login_required # Ensures only logged-in users can access logout
def logout():
    logout_user()
    return {"message": "Logout successful"}
    
    