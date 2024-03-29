# Функции для работы с асинхронным движком
from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


# DeclarativeBase - основа для создания ORM классов-таблиц
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL, String

# Загружаем информацию о бд из config.py
from config import settings

# Создаем асинхронный движок для подключения к postgres
async_engine = create_async_engine(
    url=settings.get_psycopg_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)


# Session нужна для транзакций
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(async_engine)

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

        return f"[{self.__class__.__name__}]\n\t {"\n\t,".join(columns)}"
