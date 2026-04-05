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
