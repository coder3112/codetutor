from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from src.config.settings import settings

DB = PostgresEngine(
    config={
        "database": settings.postgres_db,
        "user": settings.postgres_user,
        "password": settings.postgres_password,
        "host": settings.postgres_host,
        "port": settings.postgres_port,
    }
)

APP_REGISTRY = AppRegistry(
    apps=[
        "piccolo_admin.piccolo_app",
        "piccolo.apps.user.piccolo_app",
        "src.models.piccolo_app",
    ]
)
