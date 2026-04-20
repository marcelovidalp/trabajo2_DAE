import os
from app import create_app, db

app = create_app()


@app.cli.command("init-db")
def init_db():
    """Crea todas las tablas en la base de datos."""
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada.")


@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500 con más información."""
    db.session.rollback()
    return {
        "error": "Internal Server Error",
        "message": "Ocurrió un error interno. Por favor, contacta al administrador.",
        "status": 500
    }, 500


@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404."""
    return {
        "error": "Not Found",
        "message": "La página solicitada no existe.",
        "status": 404
    }, 404


if __name__ == "__main__":
    # En desarrollo: debug=True, en producción: debug=False (gunicorn)
    debug_mode = os.getenv("FLASK_ENV") == "development"
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=debug_mode
    )
