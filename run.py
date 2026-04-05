from app import create_app, db

app = create_app()


@app.cli.command("init-db")
def init_db():
    """Crea todas las tablas en la base de datos."""
    db.create_all()
    print("Base de datos inicializada.")


if __name__ == "__main__":
    app.run(debug=True)
