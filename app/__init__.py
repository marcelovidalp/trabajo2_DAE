from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    from app.routes.main import main_bp
    from app.routes.incidencias import incidencias_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(incidencias_bp, url_prefix="/incidencias")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
