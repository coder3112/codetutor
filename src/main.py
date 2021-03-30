"""
Server Init file.
"""
import logging
import sys
from pathlib import Path

from fastapi import FastAPI

from src.api.profile.routes import router as profile_router
from src.api.users.routes import router as user_router
from src.api.videos.routes import router as course_router
from src.config.settings import settings
from src.custom_logging import custom_logging

# Start Logger
logger = logging.getLogger(__name__)
config_path = Path(__file__).absolute().with_name("logging_config.json")

try:
    app: FastAPI = FastAPI(name=settings.name, title=settings.name)
    logger = custom_logging.CustomizeLogger.make_logger(config_path)
    # logger.add(f"/var/{settings.name.lower()}.log")
    logger.add(sys.stdout)
    logger.add(sys.stderr)
    logger.info("Initialized app")
except ModuleNotFoundError:
    logger.error("FastAPI likely not found")
    sys.exit(1)


try:
    app.include_router(user_router, tags=["Auth"])
    logger.info("Added user router")
except Exception as exception:
    logger.error(f"Could not add user router\n{exception}")
    sys.exit(1)

try:
    app.include_router(profile_router, tags=["Auth"])
    logger.info("Added profile router")
except Exception as exception:
    logger.error(f"Could not add profile router\n{exception}")
    sys.exit(1)

try:
    app.include_router(course_router, tags=["Courses"])
    logger.info("Added course router")
except Exception as exception:
    logger.error(f"Could not add course router\n{exception}")
    sys.exit(1)


@app.get("/", tags=["Default"])
def read_root_url():
    return {"message": "Welcome to CodeTutor"}
