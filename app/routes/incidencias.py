from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Incidencia, Area

incidencias_bp = Blueprint("incidencias", __name__)


@incidencias_bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    areas = Area.query.all()
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "").strip()
        prioridad = request.form.get("prioridad", "media")
        reportado_por = request.form.get("reportado_por", "").strip()
        email_reportante = request.form.get("email_reportante", "").strip()
        area_id = request.form.get("area_id") or None

        if not all([titulo, descripcion, categoria, reportado_por, email_reportante]):
            flash("Todos los campos obligatorios deben completarse.", "danger")
            return render_template("incidencias/nueva.html", areas=areas)

        incidencia = Incidencia(
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad,
            reportado_por=reportado_por,
            email_reportante=email_reportante,
            area_id=area_id,
        )
        db.session.add(incidencia)
        db.session.commit()
        flash("Incidencia reportada exitosamente.", "success")
        return redirect(url_for("main.index"))

    return render_template("incidencias/nueva.html", areas=areas)


@incidencias_bp.route("/<int:id>")
def detalle(id):
    incidencia = Incidencia.query.get_or_404(id)
    return render_template("incidencias/detalle.html", incidencia=incidencia)
