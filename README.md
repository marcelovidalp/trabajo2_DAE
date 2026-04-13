# Sistema de Registro de Incidencias Empresariales

Aplicación web desarrollada con Flask para que los empleados de una empresa puedan reportar incidencias internas y que el equipo de administración pueda visualizarlas, filtrarlas y gestionar las áreas desde un panel centralizado.

---

## Stack tecnológico

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail_SMTP-D14836?style=for-the-badge&logo=gmail&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

</div>

| Capa | Tecnología |
|---|---|
| Backend | Python 3 + Flask 3 |
| ORM / Base de datos | Flask-SQLAlchemy + PostgreSQL (SQLite en desarrollo local) |
| Plantillas | Jinja2 + Bootstrap 5 |
| Correo electrónico | Flask-Mail + Gmail App Password (SMTP TLS) |
| Despliegue | Railway — detecta `Procfile` y ejecuta gunicorn automáticamente |

---

## Descripción general

El sistema permite registrar incidencias operativas o técnicas indicando título, descripción, categoría, prioridad, área responsable y datos del reportante. Un panel de administración centraliza todas las incidencias con capacidad de filtrado, y una sección dedicada permite gestionar las áreas de la empresa.

---

## Estructura del proyecto

```
trabajo2_DAE/
├── app/
│   ├── __init__.py          # App factory: inicializa db, mail y blueprints
│   ├── models.py            # Modelos SQLAlchemy: Incidencia, Area
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Rutas raíz: index, health check
│   │   ├── incidencias.py   # Crear y ver incidencias
│   │   └── admin.py         # Panel de administración y gestión de áreas
│   ├── templates/
│   │   ├── base.html                  # Layout base con navbar y flash messages
│   │   ├── index.html                 # Página de inicio
│   │   ├── incidencias/
│   │   │   └── nueva.html             # Formulario de nueva incidencia
│   │   └── admin/
│   │       ├── panel.html             # Tabla de incidencias con filtros
│   │       └── areas.html             # CRUD de áreas
│   └── static/
│       └── css/style.css              # Estilos personalizados
├── config.py                # Configuración desde variables de entorno
├── run.py                   # Punto de entrada + comando CLI init-db
├── Procfile                 # Comando de inicio para Railway/Heroku
├── requirements.txt         # Dependencias Python
├── .env                     # Variables de entorno locales (no versionado)
└── .gitignore
```

---

## Modelos de datos

### `Area`
Representa un departamento o área de la empresa.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer PK | Identificador único |
| `nombre` | String(100) | Nombre del área, único |
| `email_responsable` | String(150) | Email del responsable del área |

### `Incidencia`
Registro de una incidencia reportada por un empleado.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer PK | Identificador único |
| `titulo` | String(200) | Título descriptivo |
| `descripcion` | Text | Detalle completo de la incidencia |
| `categoria` | String(100) | Tipo o clasificación |
| `prioridad` | String(20) | `baja`, `media`, `alta`, `critica` |
| `estado` | String(20) | `abierta`, `en_progreso`, `resuelta`, `cerrada` |
| `reportado_por` | String(150) | Nombre del reportante |
| `email_reportante` | String(150) | Email del reportante |
| `responsable_email` | String(150) | Email del responsable asignado (opcional) |
| `area_id` | FK → Area | Área asociada (opcional) |
| `fecha_creacion` | DateTime | Timestamp automático de creación |
| `fecha_actualizacion` | DateTime | Timestamp de última modificación |

---

## Rutas implementadas

| Método | URL | Descripción |
|---|---|---|
| `GET` | `/` | Página de inicio |
| `GET` | `/health` | Health check — devuelve `{"status": "ok"}` |
| `GET` | `/incidencias/nueva` | Formulario para reportar incidencia |
| `POST` | `/incidencias/nueva` | Procesamiento y guardado de la incidencia |
| `GET` | `/incidencias/<id>` | Vista de detalle de una incidencia |
| `GET` | `/admin/` | Panel de administración con filtros |
| `GET/POST` | `/admin/areas` | Listado y creación de áreas |
| `POST` | `/admin/areas/<id>/eliminar` | Eliminación de un área |

---

## Funcionalidades implementadas

### Reporte de incidencias
El formulario en `/incidencias/nueva` permite ingresar todos los datos de una incidencia. Valida que los campos obligatorios (título, descripción, categoría, nombre y email del reportante) estén completos antes de persistir el registro. Muestra mensajes de éxito o error mediante flash messages de Bootstrap.

### Panel de administración
El panel en `/admin/` presenta todas las incidencias en una tabla ordenada por fecha de creación descendente. Permite filtrar simultáneamente por:
- **Estado:** abierta, en progreso, resuelta, cerrada
- **Prioridad:** baja, media, alta, crítica
- **Área:** cualquiera de las áreas registradas en la base de datos

Cada incidencia muestra su id, título, categoría, prioridad con badge de color según nivel, estado, área y fecha de creación.

### Gestión de áreas
La sección `/admin/areas` ofrece un formulario para registrar nuevas áreas indicando nombre y email del responsable. Valida que el nombre sea único. La tabla lateral muestra todas las áreas con la cantidad de incidencias asociadas. Un área solo puede eliminarse si no tiene incidencias vinculadas, tanto a nivel de UI (botón deshabilitado) como a nivel de servidor.

### Configuración de entorno
La aplicación detecta automáticamente el entorno:
- **Producción (Railway):** usa `DATABASE_URL` inyectada por el servicio PostgreSQL de Railway, con compatibilidad automática para el driver `psycopg3`.
- **Desarrollo local:** cae en SQLite (`instance/incidencias.db`) si no hay `DATABASE_URL` configurada.

Flask-Mail está configurado para enviar notificaciones vía SMTP de Gmail con soporte TLS en el puerto 587.

---

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

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=una-clave-secreta-segura

# Omitir para usar SQLite en local
# DATABASE_URL=postgresql+psycopg://usuario:contrasena@host:5432/nombre_db

MAIL_USERNAME=tucorreo@gmail.com
MAIL_PASSWORD=tu-app-password-de-gmail
```

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Flask para sesiones y cookies |
| `DATABASE_URL` | URL de conexión a PostgreSQL (opcional en local) |
| `MAIL_USERNAME` | Correo Gmail para enviar notificaciones |
| `MAIL_PASSWORD` | App Password de Gmail (no la contraseña normal) |

### 4. Inicializar la base de datos

```bash
flask --app run init-db
```

### 5. Ejecutar el servidor de desarrollo

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`.

---

## Configurar Gmail App Password

1. Activar la verificación en dos pasos en tu cuenta Google.
2. Ir a **Mi cuenta → Seguridad → Contraseñas de aplicación**.
3. Generar una contraseña para la aplicación "Correo".
4. Usar esa contraseña (16 caracteres) como valor de `MAIL_PASSWORD`.

---

## Despliegue en Railway

1. Crear un nuevo proyecto en [railway.app](https://railway.app) y conectar este repositorio.
2. Agregar un servicio de **PostgreSQL** desde el panel — Railway inyecta `DATABASE_URL` automáticamente.
3. Configurar `SECRET_KEY`, `MAIL_USERNAME` y `MAIL_PASSWORD` en las variables de entorno del proyecto.
4. Railway detecta el `Procfile` y ejecuta `gunicorn run:app` en cada deploy.

---

## Dependencias

```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Mail==0.10.0
psycopg[binary]>=3.2.10
python-dotenv==1.0.1
gunicorn==22.0.0
```
