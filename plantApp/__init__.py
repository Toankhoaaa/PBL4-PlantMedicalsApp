# app/__init__.py
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .config import Config
from .extensions import db, migrate
from .models import Plant, MedicinalUse
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Đăng ký blueprint cho các route
    app.register_blueprint(main)

    # Khởi tạo Flask-Admin
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

    # Thêm model vào trang admin
    from .models import Plant, MedicinalUse, ChemicalComponent, Region, PlantRegion

    admin.add_view(ModelView(Plant, db.session))
    admin.add_view(ModelView(MedicinalUse, db.session))
    admin.add_view(ModelView(ChemicalComponent, db.session))
    admin.add_view(ModelView(Region, db.session))
    admin.add_view(ModelView(PlantRegion, db.session))

    return app
