from botocore.exceptions import ClientError
from .client import get_dynamodb_client
from .schema import TABLE_SCHEMA, TABLE_NAME

def ensure_table_and_gsis():
    client = get_dynamodb_client()

    # 1️⃣ Check if table exists
    try:
        table_desc = client.describe_table(TableName=TABLE_NAME)
        print(f"Table {TABLE_NAME} already exists.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print(f"Creating table {TABLE_NAME}...")
            client.create_table(**TABLE_SCHEMA)
            waiter = client.get_waiter("table_exists")
            waiter.wait(TableName=TABLE_NAME)
            print("Table created successfully!")
            table_desc = client.describe_table(TableName=TABLE_NAME)
        else:
            raise

    # 2️⃣ Check GSIs
    existing_indexes = table_desc["Table"].get("GlobalSecondaryIndexes", [])
    existing_index_names = [i["IndexName"] for i in existing_indexes]

    for gsi in TABLE_SCHEMA.get("GlobalSecondaryIndexes", []):
        if gsi["IndexName"] not in existing_index_names:
            print(f"GSI {gsi['IndexName']} missing, creating...")
            # DynamoDB only allows adding GSI after table creation
            client.update_table(
                TableName=TABLE_NAME,
                AttributeDefinitions=TABLE_SCHEMA["AttributeDefinitions"],
                GlobalSecondaryIndexUpdates=[
                    {"Create": gsi}
                ]
            )
            # Wait for GSI to be ACTIVE
            waiter = client.get_waiter("table_exists")
            waiter.wait(TableName=TABLE_NAME)
            print(f"GSI {gsi['IndexName']} created!")
        else:
            print(f"GSI {gsi['IndexName']} exists.")

if __name__ == "__main__":
    ensure_table_and_gsis()