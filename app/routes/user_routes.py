from flask import Blueprint, jsonify
from app.services.user_service import get_all_users

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=["GET"])
def users():
    return jsonify(get_all_users())