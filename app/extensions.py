# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
import boto3
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
db = SQLAlchemy()


def init_dynamodb(app):
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=app.config["DYNAMODB_ENDPOINT"],
        region_name=app.config["AWS_REGION"],
        aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
    )
    logger.info('Database connected -------------------------->')
    app.dynamodb = dynamodb

def parse_date(date_string):
    provided_date = datetime.strptime(date_string, "%d%b%Y%H%M%S")
    return provided_date.date()