import os

from piccolo.conf.apps import AppConfig

import src.models.course as course
import src.models.user_profile as user_profile
from src.models.blacklistjwt import BlackListedJWTModel

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="models",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=[
        user_profile.UserProfileModel,
        course.CourseModel,
        BlackListedJWTModel,
    ],
    migration_dependencies=["piccolo.apps.user.piccolo_app"],
    commands=[],
)
