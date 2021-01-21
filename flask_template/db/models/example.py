from sqlalchemy.sql.schema import Column

from ..db import DB, MODEL


class Example(MODEL):
    id: Column = DB.Column(DB.Integer, primary_key=True)
    name: Column = DB.Column(DB.String(120))
