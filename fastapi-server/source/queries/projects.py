from sqlalchemy import select, func, Sequence, update
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import joinedload, selectinload

from database import Base, async_engine, async_session_factory
from models.workers import Workers, Developers, Testers
from models.projects import Projects, RelProjectsWorkers
from models.plan_blocks import PlanBlocks, BlockTesting, BlockBugs, PlanBlocksTransfer

from schemas.workers import WorkersByProjectDTO
from schemas.projects import ProjectAddDTO, ProjectDTO

from new_types import BugCategory, Level, SpecializationCode


async def add_project(project: ProjectAddDTO):
    session: AsyncSession
    async with async_session_factory() as session:
        project_orm = Projects(
            **project.dict()
        )

        session.add(project_orm)

        await session.commit()


async def get_projects() -> list[ProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(Projects)
        )

        result = await session.execute(query)
        projects = result.scalars().all()
        projects_dto = [ProjectDTO.model_validate(row, from_attributes=True) for row in projects]

        return projects_dto


async def get_workers(project_id: int) -> list[WorkersByProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(RelProjectsWorkers.project_hire_date, RelProjectsWorkers.project_fire_date, Workers)
            .where(RelProjectsWorkers.project_id == project_id)
            .join(Workers, RelProjectsWorkers.workers_id == Workers.id)
        )
        # # Альтернатива из урока
        # query = (
        #     select(Workers)
        #     .where(Projects.id == project_id)
        #     .options(joinedload(Workers.projects))
        # )

        result = await session.execute(query)
        workers = result.unique().scalars().all()
        workers_by_project_dto = [WorkersByProjectDTO.model_validate(row, from_attributes=True) for row in workers]

        return workers_by_project_dto


async def update_project_description(project_id: int, description: str) -> bool:
    with async_session_factory() as session:
        # TODO: maybe should be changed to basic update to reduce amount of queries
        query = (
            update(Projects).where(Projects.id == project_id).values(description=description)
        )
        await session.execute(query)
        await session.commit()

    return True
