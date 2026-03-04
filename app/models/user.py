from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.uuid, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_no = db.Column(db.Integer, unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) 
    is_verified = db.Column(db.boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.datetime, default = datetime.utcnow)
    gender = db.Column(db.String(25), nullable=True)
    dob = db.Column(db.Datetime, nullable=True)

    def set_password_hash(self,password):
        self.password_hash = generate_password_hash(password)
    def set_last_login(self):
        self.last_login = datetime.utcnow
    def generate_password_hash(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }