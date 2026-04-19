from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import UserMixin, login_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

auth_bp = Blueprint("auth", __name__)


def _is_safe_url(target):
    """Valida que la URL de redirección sea relativa al mismo host (evita Open Redirect)."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


class AdminUser(UserMixin):
    """Usuario administrador único definido por variables de entorno."""

    def __init__(self):
        self.id = "admin"

    @staticmethod
    def get():
        return AdminUser()

    def check_password(self, password):
        return password == current_app.config["ADMIN_PASSWORD"]


def load_user(user_id):
    if user_id == "admin":
        return AdminUser()
    return None


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        expected_username = current_app.config["ADMIN_USERNAME"]
        user = AdminUser()

        if username == expected_username and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            if next_page and _is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for("admin.panel"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("main.index"))
