from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.defaults.date import DateNow
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.table import Table


class BaseUser(Table, tablename="piccolo_user"):
    pass


class CourseModel(Table, tablename="courses"):
    pass


ID = "2021-03-14T19:01:37"
VERSION = "0.16.5"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="models")

    manager.add_table("UserProfileModel", tablename="profiles")

    manager.add_table("CourseModel", tablename="courses")

    manager.add_column(
        table_class_name="UserProfileModel",
        tablename="profiles",
        column_name="role",
        column_class_name="Varchar",
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="UserProfileModel",
        tablename="profiles",
        column_name="user_id",
        column_class_name="ForeignKey",
        params={
            "references": BaseUser,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="UserProfileModel",
        tablename="profiles",
        column_name="courses_bought",
        column_class_name="ForeignKey",
        params={
            "references": CourseModel,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="UserProfileModel",
        tablename="profiles",
        column_name="courses_completed",
        column_class_name="ForeignKey",
        params={
            "references": CourseModel,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="CourseModel",
        tablename="courses",
        column_name="title",
        column_class_name="Varchar",
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": True,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="CourseModel",
        tablename="courses",
        column_name="instructor",
        column_class_name="Varchar",
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="CourseModel",
        tablename="courses",
        column_name="videos",
        column_class_name="JSONB",
        params={
            "default": "{}",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="CourseModel",
        tablename="courses",
        column_name="created_at",
        column_class_name="Timestamp",
        params={
            "default": TimestampCustom(
                year=2021, month=3, day=3, hour=19, second=37, microsecond=162473
            ),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="CourseModel",
        tablename="courses",
        column_name="modified_at",
        column_class_name="Date",
        params={
            "default": DateNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    return manager
