from piccolo.columns import Integer, Text, Timestamp, Varchar
from piccolo.table import Table


class UrlRoute(Table, tablename="url_route"):
    name = Varchar(length=100)
    alias = Varchar(length=100, unique=True, index=True)
    destination_url = Text()
    expiration = Timestamp()
    created_at = Timestamp()
    hits = Integer(default=0)
