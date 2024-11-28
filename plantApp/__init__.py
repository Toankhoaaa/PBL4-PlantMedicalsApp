# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, migrate
from .models import *
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Đăng ký blueprint cho các route
    app.register_blueprint(main)
    return app
