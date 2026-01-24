from flask import Blueprint, jsonify, request, flash
from flask_cors import cross_origin
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
            return {"success": False,"message": "Email is required"}
        
        if not password:
            return {"success": False,"message": "Password is required"}
        
        #Get the user from the database
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        if not user or not check_password_hash(user.password, password):
            return {"success": False,"message": f"Invalid email or password {email}"}
        else:
            login_user(user, remember=True)
            return {"success": True,"message": f"User {user.name} logged in"}

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
            return {"success": False, "message": "User name must be between 3 and 80 chars"}

        #Check if user entered a valid email
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return {"success": False,"message": "Invalid email"}
        #Check if user entered a valid passord
        if len(password) < 8:
            return {"success": False,"message": "Passord need to be atleast 6 chars"}

        #Check if passord and confirm passord are matched
        if password != confirm:
            return {"message": "Passowrd do not match"}

        #If data is valid ad user to the database
        try:
            pass_hash = generate_password_hash(password)
            user = User(name=name, email=email, password=pass_hash)
            db.session.add(user)
            db.session.commit()
            return {"success": True,"message": f"user {name} is added to the database"}
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred during registration: {e}")
            flash("An unexpected error occurred. Please try again later.", "danger")

@login_required # Ensures only logged-in users can access logout
@cross_origin(supports_credentials=True)
@bp.post("/logout")
def logout():
    
    logout_user()
    return jsonify({"success": True, "message": "Logged out"}), 200
        
   
    
@bp.get("/get_user")
def get_user():
    if current_user.is_authenticated:
        return {"success": True, "message": str(current_user)}
    else:
        return {"success": False, "message": "Unable to load user name"}
    
    