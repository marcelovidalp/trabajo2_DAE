from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, mail
from app.models import Incidencia, Area
from flask_login import login_required
from flask_mail import Message

incidencias_bp = Blueprint("incidencias", __name__)


def _enviar_notificaciones(incidencia):
    """Envía emails de confirmación al reportante y alerta al responsable del área.
    Silencia excepciones para no interrumpir el flujo principal si el mail falla."""
    try:
        mail.send_message(
            subject=f"[Incidencias] #{incidencia.id} recibida — {incidencia.titulo}",
            recipients=[incidencia.email_reportante],
            body=(
                f"Hola {incidencia.reportado_por},\n\n"
                f"Tu incidencia fue registrada exitosamente.\n\n"
                f"  ID:        #{incidencia.id}\n"
                f"  Título:    {incidencia.titulo}\n"
                f"  Categoría: {incidencia.categoria}\n"
                f"  Prioridad: {incidencia.prioridad}\n"
                f"  Estado:    {incidencia.estado}\n"
                f"  Área:      {incidencia.area.nombre if incidencia.area else '—'}\n\n"
                f"El equipo responsable se pondrá en contacto a la brevedad.\n\n"
                f"Sistema de Incidencias Empresariales"
            ),
        )
    except Exception:
        pass

    if incidencia.responsable_email:
        try:
            mail.send_message(
                subject=f"[Incidencias] Nueva incidencia asignada — #{incidencia.id}",
                recipients=[incidencia.responsable_email],
                body=(
                    f"Se registró una nueva incidencia asignada a tu área.\n\n"
                    f"  ID:           #{incidencia.id}\n"
                    f"  Título:       {incidencia.titulo}\n"
                    f"  Descripción:  {incidencia.descripcion}\n"
                    f"  Categoría:    {incidencia.categoria}\n"
                    f"  Prioridad:    {incidencia.prioridad}\n"
                    f"  Reportado por: {incidencia.reportado_por} <{incidencia.email_reportante}>\n\n"
                    f"Ingresa al panel de administración para gestionar esta incidencia.\n\n"
                    f"Sistema de Incidencias Empresariales"
                ),
            )
        except Exception:
            pass


@incidencias_bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    areas = Area.query.all()
    categorias = Incidencia.CATEGORIAS
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "otros")
        prioridad = request.form.get("prioridad", "media")
        reportado_por = request.form.get("reportado_por", "").strip()
        email_reportante = request.form.get("email_reportante", "").strip()
        area_id = request.form.get("area_id") or None

        if categoria not in Incidencia.CATEGORIAS:
            categoria = "otros"
        if prioridad not in Incidencia.PRIORIDADES:
            prioridad = "media"

        if not all([titulo, descripcion, reportado_por, email_reportante]):
            flash("Todos los campos obligatorios deben completarse.", "danger")
            return render_template("incidencias/nueva.html", areas=areas, categorias=categorias)

        # Asignar responsable_email desde el área seleccionada (resuelve deuda técnica 2.3)
        responsable_email = None
        if area_id:
            area = Area.query.get(area_id)
            if area:
                responsable_email = area.email_responsable

        incidencia = Incidencia(
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad,
            reportado_por=reportado_por,
            email_reportante=email_reportante,
            area_id=area_id,
            responsable_email=responsable_email,
        )
        db.session.add(incidencia)
        db.session.commit()

        _enviar_notificaciones(incidencia)

        flash("Incidencia reportada exitosamente.", "success")
        return redirect(url_for("incidencias.detalle", id=incidencia.id))

    return render_template("incidencias/nueva.html", areas=areas, categorias=categorias)


@incidencias_bp.route("/<int:id>")
def detalle(id):
    incidencia = Incidencia.query.get_or_404(id)
    return render_template(
        "incidencias/detalle.html",
        incidencia=incidencia,
        estados=Incidencia.ESTADOS,
        prioridades=Incidencia.PRIORIDADES,
    )
