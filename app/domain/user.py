from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(
        self,
        id,
        email,
        password_hash,
        username=None,
        phone_no=None,
        gender=None,
        dob=None,
        role="attendee",
        is_verified=False,
        created_at=None,
        last_login=None
    ):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.username = username
        self.phone_no = phone_no
        self.gender = gender
        self.dob = dob
        self.is_verified = is_verified
        self.created_at = created_at or datetime.utcnow()
        self.last_login = last_login

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = datetime.utcnow()

