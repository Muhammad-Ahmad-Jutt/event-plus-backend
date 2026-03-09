import boto3
import os
import logging
logger = logging.getLogger(__name__)

def get_dynamodb_client():
    """
    Returns a DynamoDB client.
    Uses DynamoDB Local if endpoint is provided.
    """

    endpoint = os.getenv("DYNAMODB_ENDPOINT")

    if endpoint:
        return boto3.client(
            "dynamodb",
            endpoint_url=endpoint,
            region_name="us-east-1",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy"
        )

    return boto3.client("dynamodb")


def get_dynamodb_resource(app):
    """
    Returns DynamoDB resource for table operations.
    """

    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=app.config["DYNAMODB_ENDPOINT"],
        region_name=app.config["AWS_REGION"],
        aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
    )
    logger.info('Database connected -------------------------->')
    app.dynamodb = dynamodb
    return dynamodb
    # endpoint = os.getenv("DYNAMODB_ENDPOINT")
 
    # if endpoint:
    #     return boto3.resource(
    #         "dynamodb",
    #         endpoint_url=endpoint,
    #         region_name="us-east-1",
    #         aws_access_key_id="dummy",
    #         aws_secret_access_key="dummy"
    #     )

    # return boto3.resource("dynamodb")