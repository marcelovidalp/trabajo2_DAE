from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta sección."
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import load_user
    login_manager.user_loader(load_user)

    from app.routes.main import main_bp
    from app.routes.incidencias import incidencias_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(incidencias_bp, url_prefix="/incidencias")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
