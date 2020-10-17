from sqlalchemy.sql.schema import Column
from flask_sqlalchemy import SQLAlchemy

from ..db import DB, MODEL


t = SQLAlchemy()


class Example(MODEL):
    id: Column = DB.Column(DB.Integer, primary_key=True)
    name: Column = DB.Column(DB.String(120))
