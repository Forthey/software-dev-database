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


async def get_workers(development_id: int) -> list[WorkersByProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(RefProjectsWorkers.project_hire_date, RefProjectsWorkers.project_fire_date, Workers).
            where(RefProjectsWorkers.project_id == development_id).
            join(Workers, RefProjectsWorkers.workers_id == Workers.id)
        )

        result = await session.execute(query)
        workers = result.scalars().all()
        workers_by_project_dto = [WorkersByProjectDTO.model_validate(row, from_attributes=True) for row in workers]

        return workers_by_project_dto
