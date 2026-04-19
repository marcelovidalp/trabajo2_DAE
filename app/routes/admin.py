from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Incidencia, Area

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
def panel():
    estado = request.args.get("estado")
    prioridad = request.args.get("prioridad")
    area_id = request.args.get("area_id")
    categoria = request.args.get("categoria")

    query = Incidencia.query
    if estado and estado in Incidencia.ESTADOS:
        query = query.filter_by(estado=estado)
    if prioridad and prioridad in Incidencia.PRIORIDADES:
        query = query.filter_by(prioridad=prioridad)
    if area_id:
        query = query.filter_by(area_id=area_id)
    if categoria and categoria in Incidencia.CATEGORIAS:
        query = query.filter_by(categoria=categoria)

    incidencias = query.order_by(Incidencia.fecha_creacion.desc()).all()
    areas = Area.query.all()

    stats = {
        "total": Incidencia.query.count(),
        "abiertas": Incidencia.query.filter_by(estado="abierta").count(),
        "en_progreso": Incidencia.query.filter_by(estado="en_progreso").count(),
        "criticas": Incidencia.query.filter_by(prioridad="critica").count(),
        "resueltas": Incidencia.query.filter_by(estado="resuelta").count(),
    }

    return render_template(
        "admin/panel.html",
        incidencias=incidencias,
        areas=areas,
        estados=Incidencia.ESTADOS,
        prioridades=Incidencia.PRIORIDADES,
        categorias=Incidencia.CATEGORIAS,
        stats=stats,
    )


@admin_bp.route("/incidencias/<int:id>/actualizar", methods=["POST"])
@login_required
def actualizar_incidencia(id):
    incidencia = Incidencia.query.get_or_404(id)
    nuevo_estado = request.form.get("estado", "").strip()
    nueva_prioridad = request.form.get("prioridad", "").strip()

    if nuevo_estado and nuevo_estado in Incidencia.ESTADOS:
        incidencia.estado = nuevo_estado
    if nueva_prioridad and nueva_prioridad in Incidencia.PRIORIDADES:
        incidencia.prioridad = nueva_prioridad

    db.session.commit()
    flash("Incidencia actualizada correctamente.", "success")
    return redirect(url_for("incidencias.detalle", id=id))


@admin_bp.route("/incidencias/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_incidencia(id):
    incidencia = Incidencia.query.get_or_404(id)
    areas = Area.query.order_by(Area.nombre).all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "").strip()
        prioridad = request.form.get("prioridad", "").strip()
        estado = request.form.get("estado", "").strip()
        reportado_por = request.form.get("reportado_por", "").strip()
        email_reportante = request.form.get("email_reportante", "").strip()
        area_id = request.form.get("area_id") or None

        if not titulo or not descripcion or not reportado_por or not email_reportante:
            flash("Los campos título, descripción, nombre y correo son obligatorios.", "danger")
            return render_template(
                "incidencias/editar.html",
                incidencia=incidencia,
                areas=areas,
                categorias=Incidencia.CATEGORIAS,
                estados=Incidencia.ESTADOS,
                prioridades=Incidencia.PRIORIDADES,
            )

        incidencia.titulo = titulo
        incidencia.descripcion = descripcion
        if categoria in Incidencia.CATEGORIAS:
            incidencia.categoria = categoria
        if prioridad in Incidencia.PRIORIDADES:
            incidencia.prioridad = prioridad
        if estado in Incidencia.ESTADOS:
            incidencia.estado = estado
        incidencia.reportado_por = reportado_por
        incidencia.email_reportante = email_reportante
        incidencia.area_id = int(area_id) if area_id else None
        if area_id:
            area = Area.query.get(int(area_id))
            incidencia.responsable_email = area.email_responsable if area else None
        else:
            incidencia.responsable_email = None

        db.session.commit()
        flash("Incidencia actualizada correctamente.", "success")
        return redirect(url_for("incidencias.detalle", id=id))

    return render_template(
        "incidencias/editar.html",
        incidencia=incidencia,
        areas=areas,
        categorias=Incidencia.CATEGORIAS,
        estados=Incidencia.ESTADOS,
        prioridades=Incidencia.PRIORIDADES,
    )


@admin_bp.route("/incidencias/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_incidencia(id):
    incidencia = Incidencia.query.get_or_404(id)
    db.session.delete(incidencia)
    db.session.commit()
    flash(f"Incidencia #{id} eliminada correctamente.", "success")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/areas", methods=["GET", "POST"])
@login_required
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


@admin_bp.route("/incidencias/<int:id>/estado", methods=["POST"])
def actualizar_estado(id):
    incidencia = Incidencia.query.get_or_404(id)
    nuevo_estado = request.form.get("estado", "").strip()

    if nuevo_estado not in Incidencia.ESTADOS:
        flash(f"Estado '{nuevo_estado}' no es válido.", "danger")
        return redirect(url_for("admin.panel"))

    incidencia.estado = nuevo_estado
    db.session.commit()
    flash(f"Estado actualizado a '{nuevo_estado}'.", "success")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/incidencias/<int:id>/prioridad", methods=["POST"])
def actualizar_prioridad(id):
    incidencia = Incidencia.query.get_or_404(id)
    nueva_prioridad = request.form.get("prioridad", "").strip()

    if nueva_prioridad not in Incidencia.PRIORIDADES:
        flash(f"Prioridad '{nueva_prioridad}' no es válida.", "danger")
        return redirect(url_for("admin.panel"))

    incidencia.prioridad = nueva_prioridad
    db.session.commit()
    flash(f"Prioridad actualizada a '{nueva_prioridad}'.", "success")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/areas/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_area(id):
    area = Area.query.get_or_404(id)
    if area.incidencias:
        flash(f"No se puede eliminar '{area.nombre}': tiene incidencias asociadas.", "danger")
    else:
        db.session.delete(area)
        db.session.commit()
        flash(f"Area '{area.nombre}' eliminada.", "success")
    return redirect(url_for("admin.areas"))

