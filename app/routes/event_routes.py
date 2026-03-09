from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

event_bp = Blueprint("events", __name__)



@event_bp.route("/create", methods=["POST"])
@jwt_required()
def create_event():

    data = request.get_json()
    current_user = get_jwt_identity()

    user_name = current_app.auth_service.user_repository.get_user_name_by_id(current_user)
    event_service = current_app.event_service
    event = event_service.create_event(
        title=data["title"],
        description=data.get("description"),
        event_start_datetime=data["event_start_datetime"],
        event_end_datetime=data["event_end_datetime"],
        no_of_participants_allowed=data.get("no_of_participants_allowed", 10),
        organizer_id=current_user,
        organizer_name=user_name,
        organizing_for=data.get("organizing_for", "self")
    )
    if not event:
        return jsonify({"success": False, "message": "Failed to create event"}), 400

    return jsonify({"success": True, "event_id": event.id}), 201

@event_bp.route("/start_event/<event_id>", methods=["PUT"])
@jwt_required()
def start_event(event_id):
    current_user = get_jwt_identity()
    event = current_app.event_service.by_id(event_id)
    if not event:
        return jsonify({"success": False, "message": "Event not found"}), 404
    if event.organizer_id != current_user:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    if event.status != 'scheduled':
        return jsonify({"success": False, "message": "Only scheduled events can be started"}), 400 
    if event.event_start_datetime > datetime.utcnow():
        return jsonify({"success": False, "message": "Event cannot be started before its start datetime"}), 400
    if event.event_end_datetime < datetime.utcnow():
        return jsonify({"success": False, "message": "Event cannot be started after its end datetime"}), 400
    if event.status == 'running':
        return jsonify({"success": False, "message": "Event is already running"}), 400
    if event.status == 'scheduled' and event.event_start_datetime <= datetime.utcnow() and event.event_end_datetime >= datetime.utcnow():
        current_app.event_service.update_event(event_id, status='running')
        room_id =current_app.event_service.create_room_for_event(event_id, current_user)
        return jsonify({"success": True, "message": "Event started successfully", "room_id": room_id}), 200
    