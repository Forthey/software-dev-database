from sqlalchemy import select, func, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import joinedload, selectinload

from database import Base, async_engine, async_session_factory
from models.workers import Workers
from models.projects import Projects
from models.plan_blocks import PlanBlocks, BlockTesting, BlockBugs, PlanBlocksTransfer


class AsyncORM:
    """
    TODO: RE DESCRIBE FUNCTIONS, BECAUSE I TRIED TO MAKE PROGRAM LOGIC IN ORM
    THESE FUNCTIONS SHOULD BE IN SERVER (PROGRAM) LOGIC, IN THIS CLASS ONLY QUERIES
    """

    #
    # Table creating
    #

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
