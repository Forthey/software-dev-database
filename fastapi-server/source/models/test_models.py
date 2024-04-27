import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column, Mapped

from database import Base


IntPrimKey = Annotated[int, mapped_column(primary_key=True)]


class TestModel1000(Base):
    __tablename__ = "test_model_1000"

    id: Mapped[IntPrimKey]
    name: Mapped[str]
    some_string: Mapped[str]
    date: Mapped[datetime.datetime]
    fake_unique: Mapped[str]


class TestModel10000(Base):
    __tablename__ = "test_model_10000"

    id: Mapped[IntPrimKey]
    name: Mapped[str]
    some_string: Mapped[str]
    date: Mapped[datetime.datetime]
    fake_unique: Mapped[str]


class TestModel100000(Base):
    __tablename__ = "test_model_100000"

    id: Mapped[IntPrimKey]
    name: Mapped[str]
    some_string: Mapped[str]
    date: Mapped[datetime.datetime]
    fake_unique: Mapped[str]
