import os

MYSQL_CONFIG = {
    "host": os.environ.get("COSTOS_DB_HOST", "190.228.29.57"),
    "port": int(os.environ.get("COSTOS_DB_PORT", "3306")),
    "user": os.environ.get("COSTOS_DB_USER", "costosup"),
    "password": os.environ.get("COSTOS_DB_PASSWORD", "UPcostos123"),
    "database": os.environ.get("COSTOS_DB_NAME", "as400"),
    "autocommit": False,
}
MYSQL_HOST = MYSQL_CONFIG.get("host", "desconocido")
SECRET_KEY = os.environ.get("COSTOS_SECRET_KEY", "pruebas-up-talp-costos2025")
