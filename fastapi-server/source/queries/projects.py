import datetime

from sqlalchemy import select, func, update, text, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import joinedload, selectinload

from engine import async_session_factory
from models.workers import WorkersORM
from models.projects import ProjectsORM, RelProjectsWorkersORM
from models.plan_blocks import PlanBlocksORM, BlockTestingORM, BlockBugsORM, PlanBlocksTransferORM


from schemas.all import ProjectAddDTO, ProjectDTO, WorkerByProjectDTO

from new_types import BugCategory, Level, SpecializationCode, ResultInfo
from schemas.plan_blocks import PlanBlockDTO


async def get_projects() -> list[ProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(ProjectsORM)
        )

        result = await session.execute(query)
        projects = result.scalars().all()

        projects_dto = [ProjectDTO.model_validate(row, from_attributes=True) for row in projects]

        return projects_dto


async def get_project(project_id: int) -> ProjectDTO:
    session: AsyncSession
    async with async_session_factory() as session:
        project_orm = await session.get(ProjectsORM, project_id)

        project_dto = ProjectDTO.model_validate(project_orm, from_attributes=True)

        await session.commit()

        return project_dto


async def search_projects(name_mask: str) -> list[ProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(ProjectsORM)
            .where(ProjectsORM.name.icontains(name_mask))
        )

        projects_orm = (await session.execute(query)).scalars().all()

        return [ProjectDTO.model_validate(project, from_attributes=True) for project in projects_orm]


async def add_project(project: ProjectAddDTO) -> ResultInfo:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(ProjectsORM)
            .where(project.name == ProjectsORM.name)
        )

        if (await session.execute(query)).all():
            await session.commit()
            return ResultInfo.failure

        project_orm = ProjectsORM(
            **project.dict()
        )

        session.add(project_orm)

        await session.commit()

        return ResultInfo.success


async def close_project(project_id: int):
    session: AsyncSession
    async with async_session_factory() as session:
        project_query = (
            update(ProjectsORM)
            .where(ProjectsORM.id == project_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
        )
        workers_query = (
            update(RelProjectsWorkersORM)
            .where(RelProjectsWorkersORM.project_id == project_id)
            .values(project_fire_date=datetime.datetime.now(datetime.UTC))
        )

        await session.execute(project_query)
        await session.execute(workers_query)

        await session.commit()


async def get_workers_from_project(project_id: int) -> list[WorkerByProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM.__table__.columns, RelProjectsWorkersORM.project_hire_date, RelProjectsWorkersORM.project_fire_date)
            .select_from(RelProjectsWorkersORM)
            .where(RelProjectsWorkersORM.project_id == project_id and RelProjectsWorkersORM.project_fire_date == None)
            .join(WorkersORM, RelProjectsWorkersORM.worker_id == WorkersORM.id)
        )

        result = await session.execute(query)

        workers_orm = result.all()

        print(f"{workers_orm=}")
        workers_dto = [WorkerByProjectDTO.model_validate(worker_orm, from_attributes=True) for worker_orm in workers_orm]

        await session.commit()

        return workers_dto


async def get_plan_blocks_from_project(project_id: int) -> list[PlanBlockDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(PlanBlocksORM)
            .where(PlanBlocksORM.project_id == project_id)
        )

        plan_blocks_orm = (await session.execute(query)).scalars().all()

        await session.commit()
        return [PlanBlockDTO.model_validate(plan_block, from_attributes=True) for plan_block in plan_blocks_orm]


async def update_project_description(project_id: int, description: str) -> bool:
    with async_session_factory() as session:
        query = (
            update(ProjectsORM).where(ProjectsORM.id == project_id).values(description=description)
        )
        await session.execute(query)

        await session.commit()

    return True
