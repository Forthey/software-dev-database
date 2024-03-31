from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing_extensions import AsyncGenerator

# Загружаем информацию о бд из config.py
from config import settings

# Создаем асинхронный движок для подключения к postgres
async_engine = create_async_engine(
    url=settings.get_psycopg_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)


# Session нужна для транзакций
async_session_factory = async_sessionmaker(async_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_session_factory()

    async with async_session:
        try:
            yield async_session
            await async_session.commit()
        except SQLAlchemyError as exc:
            await async_session.rollback()
            raise exc
        finally:
            await async_session.close()