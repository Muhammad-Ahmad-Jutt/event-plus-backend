from flask import Blueprint, request, jsonify, current_app
from app.services import authentication_service

user_bp = Blueprint("users", __name__)


@user_bp.route("/register", methods=["POST"])
def register_user():

    data = request.get_json()

    auth_service = current_app.auth_service   # ✅ get instance

    user = auth_service.register(
        email=data["email"],
        username=data["username"],
        password=data["password"],
        dob=data.get("dob"),
        gender=data.get("gender"),
        phone_no=data.get("phone_no"),
    )

    return jsonify({"success": True, "user_id": user.id}), 201


@user_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    auth_service = current_app.auth_service

    token = auth_service.login(
        email=data["email"],
        password=data["password"],
    )

    return jsonify({"access_token": token})