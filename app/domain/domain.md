1️⃣ Domain Layer
📌 What goes inside domain/

Pure business models and business rules.

Think:

“What is my system made of?”

Examples:

# domain/user.py

class User:
    def __init__(self, id, email, password_hash, role):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def is_organizer(self):
        return self.role == "organizer"
✅ Domain Contains:

Entities (User, Event, Invitation)

Business logic methods

Value objects

Enums (UserRole, EventStatus)

❌ Domain Should NOT Contain:

Database code

Flask request/response

JWT logic

HTTP status codes

boto3 calls

JSON formatting

Domain must be pure Python.