import uuid
from flask_jwt_extended import create_access_token
from app.domain.user import User


class AuthService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register(self, email, username, password, dob, gender, phone_no):

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=None,
            username=username,
            dob=dob,
            gender=gender,
            phone_no=phone_no,
        )

        user.set_password(password)

        self.user_repository.save(user)

        return user

    def login(self, email, password):

        user = self.user_repository.get_by_email(email)

        if not user:
            raise Exception("User not found")

        if not user.check_password(password):
            raise Exception("Invalid credentials")

        user.update_last_login()
        self.user_repository.save(user)

        token = create_access_token(
            identity=user.id
        )

        return token
    
#  So this the stateless jwt token based authentication service.
# logout will be handled on the client side by simply deleting the token from the front end. 
