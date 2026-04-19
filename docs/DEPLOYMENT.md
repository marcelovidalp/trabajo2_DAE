# Guía de despliegue y notificaciones por email

Sistema de Registro de Incidencias — InciTrack  
Desarrollo de Aplicaciones Empresariales · 2026

---

## Índice

1. [Notificaciones por email (Gmail SMTP)](#1-notificaciones-por-email-gmail-smtp)
2. [Despliegue en Railway](#2-despliegue-en-railway)
3. [Variables de entorno — referencia completa](#3-variables-de-entorno--referencia-completa)
4. [Verificación post-despliegue](#4-verificación-post-despliegue)

---

## 1. Notificaciones por email (Gmail SMTP)

La aplicación usa **Flask-Mail** con el servidor SMTP de Gmail para enviar dos tipos de notificación automática cada vez que se registra una incidencia:

| Destinatario | Cuándo | Contenido |
|---|---|---|
| Reportante | Al crear la incidencia | Confirmación de recepción con los datos del ticket |
| Responsable del área | Al crear la incidencia (si tiene área asignada) | Alerta con descripción completa y datos del reportante |

### 1.1 Crear una App Password de Gmail

Gmail no permite usar la contraseña normal de la cuenta para SMTP. Se requiere una **contraseña de aplicación** (App Password), que es independiente de la contraseña principal.

**Requisito previo:** la cuenta de Gmail debe tener activada la verificación en dos pasos.

**Pasos:**

1. Ir a [myaccount.google.com](https://myaccount.google.com) e iniciar sesión con la cuenta que enviará los correos.
2. Navegar a **Seguridad** → **Verificación en dos pasos** y activarla si no lo está.
3. En la misma sección de Seguridad, buscar **Contraseñas de aplicación** (aparece solo después de activar 2FA).
4. En el campo *Seleccionar aplicación* elegir **Correo** y en *Seleccionar dispositivo* elegir **Otro** → escribir `InciTrack`.
5. Hacer clic en **Generar**.
6. Copiar la contraseña de 16 caracteres que aparece (formato `xxxx xxxx xxxx xxxx`).

> Esta contraseña solo se muestra una vez. Guárdela de inmediato.

### 1.2 Configurar el archivo `.env` (desarrollo local)

Crear o editar el archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=reemplazar-con-una-clave-larga-y-aleatoria

MAIL_USERNAME=tucorreo@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx

ADMIN_USERNAME=admin
ADMIN_PASSWORD=contraseña-segura-del-panel
```

> El archivo `.env` está en `.gitignore` y no se sube al repositorio.

### 1.3 Probar el envío en local

```bash
# Activar el entorno virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# Inicializar la base de datos (solo la primera vez)
flask --app run init-db

# Levantar el servidor
python run.py
```

1. Abrir `http://localhost:5000`.
2. Crear un área con un email de responsable real (puede ser el mismo correo de prueba).
3. Completar el formulario de nueva incidencia asignándola al área creada.
4. Verificar que lleguen dos correos: uno al email del reportante y otro al email del responsable.

### 1.4 Comportamiento si el email no está configurado

Si `MAIL_USERNAME` o `MAIL_PASSWORD` no están definidas, el envío falla silenciosamente. La incidencia **se guarda igual** en la base de datos; solo se omite la notificación. Esto permite usar la aplicación en local sin configurar email.

---

## 2. Despliegue en Railway

Railway detecta el `Procfile` del proyecto y ejecuta `gunicorn run:app` automáticamente en cada deploy. La base de datos PostgreSQL se inyecta como variable de entorno.

### 2.1 Requisitos previos

- Cuenta en [railway.app](https://railway.app) (plan gratuito es suficiente para pruebas).
- Repositorio del proyecto subido a GitHub.
- App Password de Gmail configurada (sección 1.1).

### 2.2 Crear el proyecto en Railway

1. Iniciar sesión en [railway.app](https://railway.app).
2. Hacer clic en **New Project** → **Deploy from GitHub repo**.
3. Autorizar Railway para acceder a la cuenta de GitHub si es la primera vez.
4. Seleccionar el repositorio `trabajo2_DAE`.
5. Railway detecta el `Procfile` y comienza el primer deploy (fallará hasta que se configuren las variables de entorno — eso es esperado).

### 2.3 Agregar la base de datos PostgreSQL

1. Dentro del proyecto en Railway, hacer clic en **+ New** → **Database** → **Add PostgreSQL**.
2. Railway crea el servicio y genera automáticamente la variable `DATABASE_URL` disponible para el servicio Flask.
3. No se necesita configuración adicional. El `config.py` del proyecto ya maneja la conversión del prefijo `postgresql://` → `postgresql+psycopg://`.

### 2.4 Configurar las variables de entorno

1. En el proyecto Railway, hacer clic en el servicio Flask (no en el de PostgreSQL).
2. Ir a la pestaña **Variables**.
3. Agregar las siguientes variables una por una con **+ New Variable**:

| Variable | Valor de ejemplo | Descripción |
|---|---|---|
| `SECRET_KEY` | `g8h2k...` (cadena aleatoria) | Clave secreta de Flask para sesiones |
| `MAIL_USERNAME` | `notificaciones@gmail.com` | Cuenta Gmail que envía los correos |
| `MAIL_PASSWORD` | `xxxx xxxx xxxx xxxx` | App Password de 16 caracteres |
| `ADMIN_USERNAME` | `admin` | Usuario del panel de administración |
| `ADMIN_PASSWORD` | `MiClave2026!` | Contraseña del panel de administración |

> `DATABASE_URL` **no** debe agregarse manualmente. Railway la inyecta automáticamente desde el servicio PostgreSQL.

Para generar una `SECRET_KEY` segura se puede usar:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2.5 Inicializar la base de datos en producción

Una vez que el deploy termine con estado **Active**, hay que crear las tablas en PostgreSQL.

1. En el proyecto Railway, seleccionar el servicio Flask.
2. Ir a la pestaña **Settings** → sección **Deploy** → **Start Command**.
3. Alternativamente, usar la terminal integrada de Railway:
   - Hacer clic en el servicio Flask → pestaña **Deploy** → ícono de terminal.
4. Ejecutar:

```bash
flask --app run init-db
```

Respuesta esperada: `Base de datos inicializada.`

> Este comando solo debe ejecutarse **una vez**. En deploys posteriores las tablas ya existen y no es necesario repetirlo.

### 2.6 Obtener la URL pública

1. En el servicio Flask, ir a la pestaña **Settings** → sección **Networking**.
2. Hacer clic en **Generate Domain**.
3. Railway asigna una URL del formato `https://nombre-proyecto.up.railway.app`.
4. Abrir esa URL en el navegador para verificar que la aplicación responde.

### 2.7 Deploys automáticos

Cada `git push` a la rama conectada (por defecto `main`) dispara un nuevo deploy automáticamente. No se necesita ninguna acción adicional.

```bash
git add .
git commit -m "feat: descripción del cambio"
git push origin main
# Railway detecta el push y redespliega en ~30 segundos
```

---

## 3. Variables de entorno — referencia completa

| Variable | Requerida | Valor por defecto | Descripción |
|---|---|---|---|
| `SECRET_KEY` | Sí | `dev-secret-key` | Clave para firmar sesiones y cookies. Cambiar siempre en producción. |
| `DATABASE_URL` | No (local) | SQLite automático | URL de conexión a PostgreSQL. Railway la inyecta automáticamente. |
| `MAIL_SERVER` | No | `smtp.gmail.com` | Servidor SMTP. |
| `MAIL_PORT` | No | `587` | Puerto SMTP con TLS. |
| `MAIL_USERNAME` | Para email | — | Cuenta Gmail remitente. |
| `MAIL_PASSWORD` | Para email | — | App Password de Gmail (16 caracteres). |
| `ADMIN_USERNAME` | No | `admin` | Nombre de usuario del panel. |
| `ADMIN_PASSWORD` | No | `changeme` | Contraseña del panel. **Cambiar siempre en producción.** |

---

## 4. Verificación post-despliegue

Una vez desplegada la aplicación, verificar cada punto:

```
[ ] La URL pública responde y muestra la página de inicio
[ ] /health responde {"status": "ok"}
[ ] El formulario de nueva incidencia guarda correctamente (aparece en el panel admin)
[ ] El panel admin exige login (redirige a /auth/login si no está autenticado)
[ ] Las credenciales ADMIN_USERNAME / ADMIN_PASSWORD definidas en Railway funcionan
[ ] Al crear una incidencia con área, llega email al responsable del área
[ ] Al crear una incidencia, llega email de confirmación al reportante
[ ] Actualizar estado/prioridad desde el detalle funciona y persiste
```

### Endpoint de salud

```
GET /health
→ 200 {"status": "ok", "message": "Sistema de incidencias funcionando"}
```

Railway puede usar este endpoint como **health check** para monitorear que la aplicación responde correctamente.
