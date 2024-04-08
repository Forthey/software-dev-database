# Функции для работы с асинхронным движком
from typing import Annotated


# DeclarativeBase - основа для создания ORM классов-таблиц
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String


MetaStr = Annotated[str, 255]
DetailedInfoStr = Annotated[str, 2000]


class Base(DeclarativeBase):
    type_annotation_map = {
        MetaStr: String(200),
        DetailedInfoStr: String(2000)
    }

    def __repr__(self):
        columns = []
        for column in self.__table__.columns.keys():
            columns.append(f"{column}={getattr(self, column)}")

        return f"[{self.__class__.__name__}]\n\t {",\n\t".join(columns)}"
