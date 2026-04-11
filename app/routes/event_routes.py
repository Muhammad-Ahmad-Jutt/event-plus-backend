from datetime import datetime, timezone
from app import socketio
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import current_utc_time, parse_event_datetime, to_dict

event_bp = Blueprint("events", __name__)



@event_bp.route("/create", methods=["POST"])
@jwt_required()
def create_event():
    try:
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

        return jsonify({"success": True, "message": "Event created successfully", "event_id": event.id}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@event_bp.route("/<string:event_id>", methods=["GET"])
@jwt_required()
def get_event(event_id):
    try:
        current_user = get_jwt_identity()

        event = current_app.event_service.by_id(event_id)
        if not event:
            return jsonify({"success": False, "message": "Event not found"}), 404

        if str(event.organizer_id) != str(current_user):
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        return jsonify({
            "success": True,
            "message": "Event retrieved successfully",
            "event": to_dict(event)
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
@event_bp.route("/events_by_organizer", methods=["GET"])
@jwt_required()
def get_events_by_organizer():
    try:
        
        current_user = get_jwt_identity()
        events = current_app.event_service.get_events_by_organizer_id(current_user)
        events_data = [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "event_start_datetime": event.event_start_datetime,
                "event_end_datetime": event.event_end_datetime,
                "organizer_id": event.organizer_id,
                "status": event.status,
                "no_of_participants_allowed": event.no_of_participants_allowed,
            }
            for event in events
        ]
        return jsonify({"success": True, "message": "Events retrieved successfully", "events": events_data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@event_bp.route("/start_event/<event_id>", methods=["PUT"])
@jwt_required()
def start_event(event_id):
    try:
        current_user = get_jwt_identity()
        event = current_app.event_service.by_id(event_id)
        if not event:
            return jsonify({"success": False, "message": "Event not found"}), 404
        if event.organizer_id != current_user:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        if event.status != 'scheduled':
            return jsonify({"success": False, "message": "Only scheduled events can be started"}), 400 
        if parse_event_datetime(event.event_start_datetime) > current_utc_time():
            return jsonify({"success": False, "message": "Event cannot be started before its start datetime"}), 400
        if parse_event_datetime(event.event_end_datetime) < current_utc_time():
            return jsonify({"success": False, "message": "Event cannot be started after its end datetime"}), 400
        if event.status == 'running':
            return jsonify({"success": False, "message": "Event is already running"}), 400
        if event.status == 'scheduled' and parse_event_datetime(event.event_start_datetime) <= current_utc_time() and parse_event_datetime(event.event_end_datetime) >= current_utc_time():
            room_id =current_app.event_service.create_room_for_event(event_id)
            current_app.event_service.update_event(event_id, room_id=room_id, status='running')
            socketio.emit(
            "event_started",
            {
                "event_id": event_id,
                "room_id": room_id
            }
        )

            return jsonify({"success": True, "message": "Event started successfully", "room_id": room_id}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
@event_bp.route("/end_event/<event_id>", methods=["PUT"])
@jwt_required()
def end_event(event_id):
    try:
        current_user = get_jwt_identity()
        event = current_app.event_service.by_id(event_id)
        if not event:
            return jsonify({"success": False, "message": "Event not found"}), 404
        if event.organizer_id != current_user:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        if event.status != 'running':
            return jsonify({"success": False, "message": "Only running events can be ended"}), 400 
        current_app.event_service.update_event(event_id, status='ended', room_id=None)
        
        return jsonify({"success": True, "message": "Event ended successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@event_bp.route("/delete_event/<event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    try:
        current_user = get_jwt_identity()
        current_app.event_service.delete_event(event_id, current_user)

        return jsonify({"success": True, "message": "Event deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@event_bp.route("/update_event/<event_id>", methods=["PUT"])
@jwt_required()
def update_event(event_id):
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        event = current_app.event_service.by_id(event_id)
        if not event:
            return jsonify({"success": False, "message": "Event not found"}), 404
        if event.organizer_id != current_user:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        if event.status == 'running':
            return jsonify({"success": False, "message": "Cannot update a running event"}), 400
        current_app.event_service.update_event(
            event_id,
            title=data.get("title"),
            description=data.get("description"),
            event_start_datetime=data.get("event_start_datetime"),
            event_end_datetime=data.get("event_end_datetime"),
            no_of_participants_allowed=data.get("no_of_participants_allowed"),
            organizing_for=data.get("organizing_for")
        )

        return jsonify({"success": True, "message": "Event updated successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500