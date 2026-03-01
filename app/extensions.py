# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
import boto3

db = SQLAlchemy()


def init_dynamodb(app):
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=app.config["DYNAMODB_ENDPOINT"],
        region_name=app.config["AWS_REGION"],
        aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
    )

    app.dynamodb = dynamodb