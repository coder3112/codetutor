from piccolo.table import Table
from piccolo.columns import Varchar


class BlackListedJWTModel(Table, tablename="blacklisted_jwt"):
    jwt = Varchar()
