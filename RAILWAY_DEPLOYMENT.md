# 🚀 Guía de Deploy en Railway

## Paso 1: Preparar el código
✅ Ya hecho:
- `init_db.py` creado para inicializar BD automáticamente
- `Procfile` actualizado con comando `release`
- `run.py` configurado para ambos entornos
- Mejorado manejo de errores en emails

## Paso 2: Configurar Variables de Entorno en Railway

En tu panel de Railway, ve a **Variables** y agrega:

### Variables OBLIGATORIAS
```
FLASK_ENV=production
SECRET_KEY=[Genera una clave segura aquí]
ADMIN_USERNAME=admin
ADMIN_PASSWORD=[Elige una contraseña fuerte]
DATABASE_URL=[Esto se configura automáticamente si usas PostgreSQL de Railway]
```

### Variables OPCIONALES (para emails)
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=contraseña-de-app-de-google
```

## Paso 3: Configurar Base de Datos en Railway

1. En el panel de Railway, haz clic en **+ Create** → **Database** → **PostgreSQL**
2. Railway automáticamente inyectará `DATABASE_URL`
3. El script `init_db.py` se ejecutará antes de gunicorn y creará todas las tablas

## Paso 4: Desplegar

1. Conecta tu repositorio GitHub a Railway
2. Selecciona la rama `develop` o `main`
3. Railway detectará automáticamente el Procfile
4. El deploy inicia automáticamente

## Paso 5: Verificar el Deploy

### Endpoints que debes probar:
- `https://tu-app.railway.app/` → Debe cargar la página de inicio
- `https://tu-app.railway.app/health` → Debe devolver `{"status": "ok"}`
- `https://tu-app.railway.app/incidencias/nueva` → Formulario de nueva incidencia

### Si ves error 500:
1. Revisa los logs en Railway: **Logs** tab
2. Verifica que DATABASE_URL esté configurado
3. Verifica que todas las variables obligatorias estén presentes

## Paso 6: Configurar HTTPS (automático en Railway)
Railway proporciona certificados SSL automáticamente para el dominio `.railway.app`

---

## 🔧 Troubleshooting

### Error: "Internal Server Error"
- Revisa los logs de Railway
- Verifica `DATABASE_URL` está configurada
- Ejecuta `python init_db.py` localmente para verificar que funciona

### Error: "sqlalchemy.exc.OperationalError: (psycopg.Error)"
- DATABASE_URL no está configurada correctamente
- Verifica que el servicio PostgreSQL en Railway esté online

### Error: "ADMIN_PASSWORD not configured"
- Falta `ADMIN_PASSWORD` en las variables de Railway
- Agrega la variable y redeploy

---

## 📝 Requisitos finales verificados:
✅ Procfile con comando `release` para init_db
✅ run.py respeta variables de entorno PORT y FLASK_ENV
✅ init_db.py crea automáticamente todas las tablas
✅ Manejo de errores mejorado (no silencia excepciones)
✅ config.py maneja correctamente postgresql URLs
✅ requirements.txt actualizado con gunicorn y psycopg
