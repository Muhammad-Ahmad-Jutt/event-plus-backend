from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt
user_bp = Blueprint("users", __name__)


@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        data = request.get_json()

        auth_service = current_app.auth_service   

        user = auth_service.register(
            email=data["email"],
            username=data["username"],
            password=data["password"],
            dob=data.get("dob"),
            gender=data.get("gender"),
            phone_no=data.get("phone_no"),
        )

        return jsonify({"success": True, "message": "User registered successfully", "user_id": user.id}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        auth_service = current_app.auth_service

        result = auth_service.login(
            email=data["email"],
            password=data["password"],
        )
        
        print('Token generated successfully---------------------------------------------------------------------------------------------', result, result['token'])
        return jsonify({"success": True, "message": "Login successful", "user": result['username'], "access_token": result['token']})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 401