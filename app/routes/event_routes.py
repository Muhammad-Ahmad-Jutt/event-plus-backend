from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

event_bp = Blueprint("events", __name__)



@event_bp.route("/create", methods=["POST"])
@jwt_required()
def create_event():

    data = request.get_json()
    current_user = get_jwt_identity()

    
    event_service = current_app.event_service
    user = current_app.auth_service.user_repository.get_by_id(current_user)
    event = event_service.create_event(
        title=data["title"],
        description=data.get("description"),
        event_start_datetime=data["event_start_datetime"],
        event_end_datetime=data["event_end_datetime"],
        no_of_participants_allowed=data.get("no_of_participants_allowed", 10),
        organizer_email=user.email,
        organizer_name=user.username,
        organizing_for=data.get("organizing_for", "self")
    )
    if not event:
        return jsonify({"success": False, "message": "Failed to create event"}), 400

    return jsonify({"success": True, "event_id": event.id}), 201