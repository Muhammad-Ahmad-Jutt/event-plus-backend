TABLE_NAME = "event_plus"

TABLE_SCHEMA = {
    "TableName": TABLE_NAME,
    "KeySchema": [
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
        {"AttributeName": "slug", "AttributeType": "S"},
        {"AttributeName": "organizer_email", "AttributeType": "S"},
        {"AttributeName": "title", "AttributeType": "S"}
    ],
    "BillingMode": "PAY_PER_REQUEST",
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "slug-index",
            "KeySchema": [
                {"AttributeName": "slug", "KeyType": "HASH"},
                {"AttributeName": "PK", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        },
        {
            "IndexName": "organizer-index",
            "KeySchema": [
                {"AttributeName": "organizer_email", "KeyType": "HASH"},
                {"AttributeName": "slug", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        },
        {
            "IndexName": "title-index",
            "KeySchema": [
                {"AttributeName": "title", "KeyType": "HASH"},
                {"AttributeName": "PK", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        },
        {
            "IndexName": "title-organizer-index",
            "KeySchema": [
                { "AttributeName": "title", "KeyType": "HASH" },
                { "AttributeName": "organizer_email", "KeyType": "RANGE" }
            ],
            "Projection": { "ProjectionType": "ALL" }
        }
    ]
}