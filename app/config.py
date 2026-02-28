import os

class Config:
    # Secret key (important for sessions / JWT later)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # Database (example: SQLite by default)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///app.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: useful for APIs
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False