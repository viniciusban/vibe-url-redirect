from piccolo.columns import Integer, Text, Timestamp, Varchar
from piccolo.table import Table

from steerer.engine import DB


class UrlRoute(Table, tablename="url_route", db=DB):
    name = Varchar(length=100)
    alias = Varchar(length=100, unique=True, index=True)
    destination_url = Text()
    expiration = Timestamp()
    created_at = Timestamp()
    hits = Integer(default=0)
