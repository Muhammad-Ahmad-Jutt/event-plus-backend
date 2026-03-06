2️⃣ Repository Layer
📌 What goes inside repository/
This layer talks to DynamoDB.
crud is in repository
Think:

“How do I store and retrieve data?”

Example:

# repository/user_repository.py

class UserRepository:
    def __init__(self, dynamodb_client):
        self.table = dynamodb_client.Table("users")

    def save(self, user):
        self.table.put_item(Item=user.__dict__)

    def get_by_email(self, email):
        response = self.table.get_item(Key={"email": email})
        return response.get("Item")
✅ Repository Contains:

DynamoDB queries

put_item

get_item

update_item

delete_item

Query logic

Scan logic

❌ Repository Should NOT Contain:

Business validation

Password hashing

JWT generation

Flask request object

HTTP status codes

Repository = data access only