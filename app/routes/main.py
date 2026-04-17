from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@main_bp.route("/health")
def health():
    return {"status": "ok", "message": "Sistema de incidencias funcionando"}, 200
