import os
from flask import Flask, current_app
from logging.config import dictConfig
from dotenv import load_dotenv
from .extensions import db
import logging
import time
# from .extensions import db, init_dynamodb
from app.infrastructure.dynamodb.setup import ensure_table_and_gsis
from app.infrastructure.dynamodb.client import get_dynamodb_resource
from app.repositories.user_repository import UserRepository
from app.services.authentication_service import AuthService
from app.repositories.event_repository import EventRepository
from app.services.event_service import EventService
from flask_jwt_extended import JWTManager
load_dotenv()  


def create_app():
    app = Flask(__name__)
    jwt = JWTManager()

    # Choose environment
    env = os.getenv("APP_ENV", "development")
    if env == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    # Ensure logs folder exists (if later adding file logging)
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Initialize logging
    dictConfig(app.config["LOGGING_CONFIG"])
    logger = logging.getLogger(__name__)
    logger.info(f"Starting app in {env.upper()} mode")
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    ensure_table_and_gsis()
    dynamodb = get_dynamodb_resource(app)
    user_repo = UserRepository(dynamodb,app.config['DYNAMODB_TABLE'])
    auth_service = AuthService(user_repo)
    app.auth_service = auth_service

    event_repo = EventRepository(dynamodb, app.config['DYNAMODB_TABLE'])
    event_service = EventService(event_repo, user_repo)
    app.event_service = event_service

    # Register middleware logging
    register_logging_middleware(app)

    # Register blueprints
    from .routes.user_routes import user_bp
    from .routes.event_routes import event_bp
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(event_bp, url_prefix="/api/events")
    return app


# ----------------------------
# Logging Middleware
# ----------------------------

def register_logging_middleware(app):
    logger = logging.getLogger("request_logger")

    @app.before_request
    def log_request():
        from flask import request
        request.start_time = time.time()

        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.path,
                "ip": request.remote_addr,
            },
        )

    @app.after_request
    def log_response(response):
        from flask import request
        duration = time.time() - request.start_time

        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            },
        )

        return response