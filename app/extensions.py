# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
import boto3
import logging
from datetime import datetime
import uuid
logger = logging.getLogger(__name__)
db = SQLAlchemy()


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
    start_datetime = parse_date(start_datetime_str)
    end_datetime = parse_date(end_datetime_str)
    if start_datetime > end_datetime:
        raise ValueError("Event start datetime cannot be after end datetime.")
    return start_datetime, end_datetime
def serialize_datetime(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value