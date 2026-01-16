from flask import Blueprint, request
from .models import User
from .extensions import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
import re

bp = Blueprint("main", __name__)

#endpoint for handling login
@bp.post("/login")
def login():
    pass

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
    