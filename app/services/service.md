3️⃣ Service Layer

This is the MOST IMPORTANT layer.
all the checking validation will go in the service layer
business logic  

📌 What goes inside services/

Business logic and orchestration.

Think:

“What should happen when user registers?”

Example:

# services/auth_service.py

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, email, password):
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise Exception("User already exists")

        password_hash = hash_password(password)

        user = User(
            id=str(uuid4()),
            email=email,
            password_hash=password_hash,
            role="attendee"
        )

        self.user_repository.save(user)

        return user
✅ Service Contains:

Validation logic

Password hashing

Token creation

Role checking

Business workflows

Calling multiple repositories

❌ Service Should NOT Contain:

Flask request object

jsonify

HTTP response

boto3

Direct DynamoDB calls

Service = business brain