# Sistema de Registro de Incidencias Empresariales

Aplicación web para reportar y gestionar incidencias internas. Construida con Flask + PostgreSQL.

## Stack

- **Backend:** Python 3 + Flask
- **Base de datos:** PostgreSQL + SQLAlchemy
- **Frontend:** Bootstrap 5 + Jinja2
- **Correo:** Flask-Mail + Gmail App Password
- **Despliegue:** Railway

## Estructura del proyecto

```
trabajo2_DAE/
├── app/
│   ├── __init__.py          # App factory, inicializa extensiones
│   ├── models.py            # Modelos SQLAlchemy (Incidencia, Area)
│   ├── routes/
│   │   ├── main.py          # Ruta raíz e index
│   │   ├── incidencias.py   # Crear y ver incidencias
│   │   └── admin.py         # Panel de administración
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── admin/
│   │       └── panel.html
│   └── static/
│       └── css/style.css
├── config.py                # Configuración desde variables de entorno
├── run.py                   # Punto de entrada + CLI
├── Procfile                 # Para Railway/Heroku
├── requirements.txt
├── .env.example
└── .gitignore
```

## Instalación local

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd trabajo2_DAE
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus credenciales
```

Variables requeridas:

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Flask |
| `DATABASE_URL` | URL de conexión PostgreSQL |
| `MAIL_USERNAME` | Correo Gmail para notificaciones |
| `MAIL_PASSWORD` | App Password de Gmail |

### 4. Inicializar la base de datos

```bash
flask --app run init-db
```

### 5. Ejecutar el servidor de desarrollo

```bash
python run.py
```

La app estará en `http://localhost:5000`.

Ruta de prueba: `GET /health` → devuelve `{"status": "ok"}`.

## Configurar Gmail App Password

1. Activar verificación en dos pasos en tu cuenta Google.
2. Ir a **Seguridad → Contraseñas de aplicación**.
3. Generar una contraseña para "Correo" + "Windows/Mac".
4. Usar esa contraseña en `MAIL_PASSWORD`.

## Despliegue en Railway

1. Crear proyecto en [railway.app](https://railway.app) y conectar el repositorio.
2. Añadir un plugin de **PostgreSQL** — Railway inyecta `DATABASE_URL` automáticamente.
3. Configurar las variables de entorno restantes en el panel de Railway.
4. Railway detecta el `Procfile` y ejecuta `gunicorn run:app`.
