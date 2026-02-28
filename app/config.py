# app/config.py

import os
import copy

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///app.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # Base Logging Config
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            },
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }


class DevelopmentConfig(Config):
    DEBUG = True

    LOGGING_CONFIG = copy.deepcopy(Config.LOGGING_CONFIG)
    LOGGING_CONFIG["root"]["level"] = "DEBUG"
    LOGGING_CONFIG["formatters"]["standard"]["format"] = \
        "[DEV] %(asctime)s - %(levelname)s - %(name)s - %(message)s"


class ProductionConfig(Config):
    DEBUG = False

    LOGGING_CONFIG = copy.deepcopy(Config.LOGGING_CONFIG)

    # Use JSON formatter in production
    LOGGING_CONFIG["handlers"]["console"]["formatter"] = "json"
    LOGGING_CONFIG["root"]["level"] = "INFO"