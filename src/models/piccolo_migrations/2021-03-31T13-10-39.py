from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2021-03-31T13:10:39"
VERSION = "0.16.5"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="models")

    manager.add_table("BlackListedJWTModel", tablename="blacklisted_jwt")

    manager.add_column(
        table_class_name="BlackListedJWTModel",
        tablename="blacklisted_jwt",
        column_name="jwt",
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

    manager.alter_column(
        table_class_name="CourseModel",
        tablename="courses",
        column_name="created_at",
        params={
            "default": TimestampCustom(
                year=2021, month=3, day=3, hour=13, second=39, microsecond=97152
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2021, month=3, day=3, hour=19, second=37, microsecond=162473
            )
        },
    )

    return manager
