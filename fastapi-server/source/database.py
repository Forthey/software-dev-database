# Функции для работы с асинхронным движком
from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Стандартные функции (в основном с поддержкой синхронного движка)
# Session - для создания сессий. sessionmaker упрощает сосздание сессий
# DeclarativeBase -
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String

# Загружаем информацию о бд из config.py
from config import settings

# Создаем асинхронный движок для подключения к postgres
async_engine = create_async_engine(
    url=settings.get_psycopg_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)

# Создаем синхронный движок для подключения (на выбор)
sync_engine = create_engine(
    url=settings.get_psycopg_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

# Session нужна для транзакций
session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)


MetaStr = Annotated[str, 255]
DetailedInfoStr = Annotated[str, 2000]


class Base(DeclarativeBase):
    type_annotation_map = {
        MetaStr: String(200),
        DetailedInfoStr: String(2000)
    }
