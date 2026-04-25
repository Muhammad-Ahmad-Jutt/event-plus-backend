# app/extensions.py

import json
from flask_sqlalchemy import SQLAlchemy
import boto3
import logging
from datetime import datetime, timezone
import uuid
from flask import current_app

from flask_socketio import SocketIO
logger = logging.getLogger(__name__)
db = SQLAlchemy()
socketio = SocketIO( cors_allowed_origins="*")


# def init_dynamodb(app):
#     dynamodb = boto3.resource(
#         "dynamodb",
#         endpoint_url=app.config["DYNAMODB_ENDPOINT"],
#         region_name=app.config["AWS_REGION"],
#         aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
#         aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
#     )
#     logger.info('Database connected -------------------------->')
#     app.dynamodb = dynamodb
#     return dynamodb
def parse_date(date_string):
    provided_date = datetime.strptime(date_string, "%d%b%Y%H%M%S")
    return provided_date.date()
def generate_slug(title):
    slug = title.lower().replace(" ", "-")
    unique_id = str(uuid.uuid4())[:8]
    return f"{slug}-{unique_id}"
def match_start_end_datetime(start_datetime_str, end_datetime_str):
    start_datetime = parse_event_datetime(start_datetime_str)
    end_datetime = parse_event_datetime(end_datetime_str)
    if start_datetime > end_datetime:
        raise ValueError("Event start datetime cannot be after end datetime.")
    return start_datetime, end_datetime
def serialize_datetime(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value

def safe_parse_iso(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        # Log invalid datetime and return None
        print(f"[WARNING] Invalid datetime string: {dt_str}")
        return None
def parse_event_datetime(date_string: str):
    

    dt = datetime.fromisoformat(date_string)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return str(dt)

def current_utc_time():
    return str(datetime.now(timezone.utc))

def convert_dict_to_json(data):
    return json.dumps(data)
def to_dict(self):
    return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "event_start_datetime": (
            self.event_start_datetime.isoformat()
            if hasattr(self.event_start_datetime, "isoformat")
            else self.event_start_datetime
        ),

        "event_end_datetime": (
            self.event_end_datetime.isoformat()
            if hasattr(self.event_end_datetime, "isoformat")
            else self.event_end_datetime
        ),

        "organizer_id": self.organizer_id,
        "status": self.status,
        "no_of_participants_allowed": self.no_of_participants_allowed,
        "room_id": self.room_id
    }

def get_current_user_name(user_id):
    user = current_app.auth_service.get_user_by_id(user_id)
    return user.username if user else "Unknown User"
