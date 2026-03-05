from app.domain.user import User


class UserRepository:

    def __init__(self, dynamodb, table_name):
        self.table = dynamodb.Table(table_name)

    def save(self, user: User):

        item = {
            "PK": f"USER#{user.id}",
            "SK": "PROFILE",
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
            "dob": str(user.dob) if user.dob else None,
            "gender": user.gender,
            "phone_no": user.phone_no,
            "last_login": str(user.last_login) if user.last_login else None,
        }

        self.table.put_item(Item=item)

    def get_by_email(self, email):

        response = self.table.scan(
            FilterExpression="email = :email",
            ExpressionAttributeValues={":email": email},
        )

        items = response.get("Items")

        if not items:
            return None

        item = items[0]

        return User(
            id=item["PK"].split("#")[1],
            email=item["email"],
            password_hash=item["password_hash"],
            username=item.get("username"),
            phone_no=item.get("phone_no"),
            gender=item.get("gender"),
            dob=item.get("dob"),
            last_login=item.get("last_login"),
        )