"""
Server Init file.
"""
import logging
import sys
from pathlib import Path

from fastapi import FastAPI

from src.api.users.routes import add_piccolo_user_crud
from src.api.users.routes import router as user_router
from src.config.settings import settings
from src.custom_logging import custom_logging

# Start Logger
logger = logging.getLogger(__name__)
config_path = Path(__file__).absolute().with_name("logging_config.json")

try:
    app: FastAPI = FastAPI(name=settings.name, title=settings.name)
    logger = custom_logging.CustomizeLogger.make_logger(config_path)
    logger.add(f"/var/{settings.name.lower()}.log")
    logger.info("Initialized app")
except ModuleNotFoundError:
    logger.error("FastAPI likely not found")
    sys.exit(1)


try:
    app.include_router(user_router, tags=["Auth"])
    logger.info("Added user router")
    add_piccolo_user_crud(app)
except Exception as exception:
    logger.error(f"Could not add user router\n{exception}")
    sys.exit(1)


@app.get("/")
def read_root_url():
    return {"message": "Welcome to CodeTutor"}
