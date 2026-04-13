from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import Incidencia, Area

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
def panel():
    estado = request.args.get("estado")
    prioridad = request.args.get("prioridad")
    area_id = request.args.get("area_id")

    query = Incidencia.query
    if estado:
        query = query.filter_by(estado=estado)
    if prioridad:
        query = query.filter_by(prioridad=prioridad)
    if area_id:
        query = query.filter_by(area_id=area_id)

    incidencias = query.order_by(Incidencia.fecha_creacion.desc()).all()
    areas = Area.query.all()
    return render_template(
        "admin/panel.html",
        incidencias=incidencias,
        areas=areas,
        estados=Incidencia.ESTADOS,
        prioridades=Incidencia.PRIORIDADES,
    )


@admin_bp.route("/areas", methods=["GET", "POST"])
def areas():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email_responsable", "").strip()

        if not nombre or not email:
            flash("Nombre y email del responsable son obligatorios.", "danger")
        elif Area.query.filter_by(nombre=nombre).first():
            flash(f"Ya existe un area con el nombre '{nombre}'.", "warning")
        else:
            db.session.add(Area(nombre=nombre, email_responsable=email))
            db.session.commit()
            flash(f"Area '{nombre}' creada correctamente.", "success")

        return redirect(url_for("admin.areas"))

    todas = Area.query.order_by(Area.nombre).all()
    return render_template("admin/areas.html", areas=todas)


@admin_bp.route("/areas/<int:id>/eliminar", methods=["POST"])
def eliminar_area(id):
    area = Area.query.get_or_404(id)
    if area.incidencias:
        flash(f"No se puede eliminar '{area.nombre}': tiene incidencias asociadas.", "danger")
    else:
        db.session.delete(area)
        db.session.commit()
        flash(f"Area '{area.nombre}' eliminada.", "success")
    return redirect(url_for("admin.areas"))
