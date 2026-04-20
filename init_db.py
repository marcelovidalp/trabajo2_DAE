#!/usr/bin/env python
"""
Script para inicializar la base de datos.
Se ejecuta automáticamente en Railway antes de iniciar la aplicación.
"""
from app import create_app, db

def init_database():
    """Crea todas las tablas en la base de datos."""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_database()
