from flask import Blueprint, request
from .models import User

bp = Blueprint("main", __name__)


@bp.post("/login")
def login():
    pass

@bp.post("/register")
def register():
    if request.method == "POST":
        name = request.get("name")
        email = request.get("email")
        password = request.get("password")
        confirm = request.get("confirm_password")
        print("Form submitted: ", name, email, password, confirm)

        return f"Recived - {email}"