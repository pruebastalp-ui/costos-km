import os
MYSQL_CONFIG = {
    "host": os.environ.get("COSTOS_DB_HOST", "localhost"),
    "port": int(os.environ.get("COSTOS_DB_PORT", "3306")),
    "user": os.environ.get("COSTOS_DB_USER", "costosup"),
    "password": os.environ.get("COSTOS_DB_PASSWORD", "upcostos123"),
    "database": os.environ.get("COSTOS_DB_NAME", "costos_mvp"),
    "autocommit": False,
}
MYSQL_HOST = MYSQL_CONFIG.get("host", "desconocido")
SECRET_KEY = os.environ.get("COSTOS_SECRET_KEY", "cambiar-esto-en-produccion")
