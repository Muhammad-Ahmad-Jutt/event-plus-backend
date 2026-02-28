#app factory
from flask import Flask
from .extensions import db
from .routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix="/api/users")

    return app