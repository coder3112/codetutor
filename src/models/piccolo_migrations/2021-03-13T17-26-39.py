from piccolo.apps.migrations.auto import MigrationManager


ID = "2021-03-13T17:26:39"
VERSION = "0.16.5"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="")

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
