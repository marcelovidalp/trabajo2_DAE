from datetime import datetime, timezone
from app import db


class Area(db.Model):
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    email_responsable = db.Column(db.String(150), nullable=False)

    incidencias = db.relationship("Incidencia", backref="area", lazy=True)

    def __repr__(self):
        return f"<Area {self.nombre}>"


class Incidencia(db.Model):
    __tablename__ = "incidencia"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    prioridad = db.Column(db.String(20), nullable=False, default="media")
    estado = db.Column(db.String(20), nullable=False, default="abierta")
    reportado_por = db.Column(db.String(150), nullable=False)
    email_reportante = db.Column(db.String(150), nullable=False)
    responsable_email = db.Column(db.String(150))
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    area_id = db.Column(db.Integer, db.ForeignKey("area.id"))

    ESTADOS = ["abierta", "en_progreso", "resuelta", "cerrada"]
    PRIORIDADES = ["baja", "media", "alta", "critica"]
    CATEGORIAS = ["hardware", "software", "red", "acceso", "seguridad", "otros"]

    def __repr__(self):
        return f"<Incidencia {self.id}: {self.titulo}>"
