from sqlalchemy import select, func, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import joinedload, selectinload

from database import Base, async_engine, async_session_factory
from models.workers import Workers, Developers, Testers
from models.projects import Projects, RefProjectsWorkers
from models.plan_blocks import PlanBlocks, BlockTesting, BlockBugs, PlanBlocksTransfer

from schemas.workers import WorkersDTO, WorkersAddDTO
from schemas.projects import ProjectAddDTO, ProjectDTO

from new_types import BugCategory, Level, SpecializationCode


async def add_worker(worker: WorkersAddDTO):
    session: AsyncSession
    async with async_session_factory() as session:
        worker_orm = Workers(
            **worker.dict()
        )

        session.add(worker_orm)

        await session.commit()


async def get_worker(worker_id: int) -> WorkersDTO:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(Workers).where(Workers.id == worker_id)
        )

        result = await session.execute(query)
        worker = result.scalars().all()[0]
        worker_dto = WorkersDTO.model_validate(worker, from_attributes=True)

        return worker_dto
