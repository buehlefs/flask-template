from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import sqltypes as sql

from ..db import MODEL, REGISTRY


# see <https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping>
class Example(MODEL):
    __tablename__ = "Example"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sql.String(120))


# see <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#integration-with-dataclasses-and-attrs>
# use this style if you have 1.4 dataclass models to migrate
@REGISTRY.mapped_as_dataclass
class TestDataclass:
    __tablename__ = "TestDataclass"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(sql.String(50), default=None)
    fullname: Mapped[str] = mapped_column(sql.String(50), default="")
    nickname: Mapped[str] = mapped_column(sql.String(12), default="")
