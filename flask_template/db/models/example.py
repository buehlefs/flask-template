from dataclasses import dataclass, field
from typing import Optional
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql import sqltypes as sql

from ..db import MODEL, REGISTRY


class Example(MODEL):
    __tablename__ = "Example"
    id: Column = Column(sql.Integer, primary_key=True)
    name: Column = Column(sql.String(120))


# only for sqlalchemy 1.4 (see <https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#example-two-dataclasses-with-declarative-table>)
# This style probably has better type hint and autocompletion support
@REGISTRY.mapped
@dataclass
class TestDataclass:
    __tablename__ = "TestDataclass"

    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(sql.Integer, primary_key=True)})
    name: Optional[str] = field(default=None, metadata={"sa": Column(sql.String(50))})
    fullname: str = field(default="", metadata={"sa": Column(sql.String(50))})
    nickname: str = field(default="", metadata={"sa": Column(sql.String(12))})
