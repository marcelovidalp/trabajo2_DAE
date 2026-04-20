# ✅ Checklist de Deployment en Railway

## Pre-deployment (Antes de pushear a GitHub)

- [ ] Verificar que `python init_db.py` ejecuta sin errores
- [ ] Verificar que `python run.py` funciona localmente
- [ ] Revisar que `.gitignore` incluya `.env` (no versionear variables secretas)
- [ ] Revisar que `requirements.txt` tiene todas las dependencias (gunicorn, psycopg, etc.)
- [ ] Commit todos los cambios al repositorio

## En Railway Dashboard

### 1. Crear proyecto
- [ ] Crear nuevo proyecto en https://railway.app
- [ ] Conectar repositorio GitHub
- [ ] Seleccionar rama (`main` o `develop`)
- [ ] Dejar que Railway auto-detecte Python

### 2. Agregar PostgreSQL
- [ ] Hacer clic en `+ New`
- [ ] Seleccionar `Database` → `PostgreSQL`
- [ ] Esperar a que se cree (tomará ~2 minutos)
- [ ] Railway inyectará automáticamente `DATABASE_URL`

### 3. Configurar Variables de Entorno
En la sección **Variables** del proyecto, agregar:

**OBLIGATORIAS:**
- [ ] `FLASK_ENV` = `production`
- [ ] `SECRET_KEY` = [Genera una clave fuerte - usa openssl rand -hex 32]
- [ ] `ADMIN_USERNAME` = `admin`
- [ ] `ADMIN_PASSWORD` = [Contraseña segura]

**OPCIONALES (para email):**
- [ ] `MAIL_USERNAME` = tu-email@gmail.com
- [ ] `MAIL_PASSWORD` = tu-app-password-gmail

### 4. Verificar Procfile
- [ ] Revisar que `Procfile` contiene:
  ```
  release: python init_db.py
  web: gunicorn run:app --bind "0.0.0.0:${PORT:-8080}"
  ```

### 5. Desplegar
- [ ] Hacer push de los cambios a GitHub
- [ ] Railway detectará automáticamente y comenzará el deploy
- [ ] Esperar a que termine el deployment (~3-5 minutos)

## Post-deployment

### Verificación inicial
- [ ] Acceder a `https://tu-app.railway.app/` 
- [ ] Verificar que carga sin errores 500
- [ ] Probar endpoint `/health` → debe devolver `{"status": "ok"}`

### Pruebas funcionales
- [ ] Crear una nueva incidencia en `/incidencias/nueva`
- [ ] Verificar que se guarda en la BD
- [ ] Ir al panel admin `/admin/` (login: admin/tu-password)
- [ ] Verificar que aparece la incidencia creada
- [ ] Probar filtros por estado, prioridad, categoría

### Verificar logs
- [ ] En Railway, ir a **Deployments** tab
- [ ] Hacer clic en el último deployment
- [ ] Revisar **Logs** si hay errores
- [ ] Buscar mensaje "✓ Base de datos inicializada correctamente"

## Si algo falla

### Error 500 al acceder a la app
1. Revisar Logs en Railway
2. Verificar que `DATABASE_URL` está configurada
3. Verificar que `SECRET_KEY` no está vacía
4. Triggear nuevo deployment (cambiar una variable y guardar)

### Error de conexión a PostgreSQL
1. Verificar que servicio PostgreSQL está online en Railway
2. Verificar que `DATABASE_URL` contiene credenciales correctas
3. En Railway, ir a PostgreSQL service → Connection string
4. Copiar la URL y usarla para verificar conexión

### Incidencias no se crean
1. Revisar que `init_db.py` ejecutó exitosamente (ver en Logs)
2. Verificar que las tablas existen en PostgreSQL
3. Revisar en Railway → PostgreSQL → Data
4. Triggear init_db manualmente: SSH a railway y ejecutar `python init_db.py`

## Rollback de emergencia
Si algo está muy roto:
1. En Railway, ir a **Deployments**
2. Seleccionar el deployment anterior (el que funcionaba)
3. Hacer clic en **Rollback**
4. La app se revertirá a la versión anterior

---

## Referencia rápida de URLs

| Endpoint | Descripción |
|----------|-----------|
| `/` | Página de inicio |
| `/health` | Health check |
| `/incidencias/nueva` | Crear incidencia |
| `/incidencias/<id>` | Ver detalle de incidencia |
| `/admin/` | Panel admin (requiere login) |
| `/admin/areas` | Gestión de áreas |
| `/auth/login` | Iniciar sesión |
| `/auth/logout` | Cerrar sesión |

---

**¡Si todo está bien, tu app está lista en producción! 🚀**
