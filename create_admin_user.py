from piccolo.apps.user.tables import BaseUser

created_user_list = BaseUser.insert(
    BaseUser(
        username="admin",
        email="admin@admin.com",
        password="adminisgr8",
        active=True,
        admin=True,
    )
).run_sync()
