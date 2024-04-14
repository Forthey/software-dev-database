import datetime

from sqlalchemy import select, func, update, text, desc, asc, insert
from sqlalchemy.exc import IntegrityError
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

from new_types import BugCategory, Level, SpecializationCode
from schemas.plan_blocks import PlanBlockDTO
from schemas.projects import ProjectOnCloseDTO


async def get_projects() -> list[ProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(ProjectsORM)
        )

        projects_orm = (await session.execute(query)).scalars().all()

        return [ProjectDTO.model_validate(row, from_attributes=True) for row in projects_orm]


async def get_project(project_id: int) -> ProjectDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        project_orm = await session.get(ProjectsORM, project_id)

        return ProjectDTO.model_validate(project_orm, from_attributes=True) if project_orm else None


async def search_projects(name_mask: str) -> list[ProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(ProjectsORM)
            .where(ProjectsORM.name.icontains(name_mask))
        )

        projects_orm = (await session.execute(query)).scalars().all()

        return [ProjectDTO.model_validate(project, from_attributes=True) for project in projects_orm]


async def add_project(project: ProjectAddDTO) -> int | None:
    session: AsyncSession
    async with async_session_factory() as session:
        try:
            query = (
                insert(ProjectsORM)
                .values(**project.model_dump())
                .returning(ProjectsORM.id)
            )

            project_id = (await session.execute(query)).scalar_one()

            await session.commit()
            return project_id
        except IntegrityError:
            return None


async def close_project(project_id: int) -> ProjectOnCloseDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        project_query = (
            update(ProjectsORM)
            .where(ProjectsORM.id == project_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(ProjectsORM.id)
        )
        workers_query = (
            update(RelProjectsWorkersORM)
            .where(RelProjectsWorkersORM.project_id == project_id)
            .values(project_fire_date=datetime.datetime.now(datetime.UTC))
            .returning(RelProjectsWorkersORM.worker_id)
        )
        plan_blocks_query = (
            update(PlanBlocksORM)
            .where(PlanBlocksORM.project_id == project_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(PlanBlocksORM.id)
        )

        project_id = (await session.execute(project_query)).scalar_one_or_none()

        if project_id is None:
            return None

        workers_id = (await session.execute(workers_query)).scalars().all()
        plan_blocks_id = (await session.execute(plan_blocks_query)).scalars().all()

        await session.commit()
        return ProjectOnCloseDTO(
            project_id=project_id,
            workers_id=workers_id,
            plan_blocks_id=plan_blocks_id
        )


async def get_workers_from_project(project_id: int) -> list[WorkerByProjectDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM.__table__.columns, RelProjectsWorkersORM.project_hire_date, RelProjectsWorkersORM.project_fire_date)
            .select_from(RelProjectsWorkersORM)
            .where(RelProjectsWorkersORM.project_id == project_id and RelProjectsWorkersORM.project_fire_date == None)
            .join(WorkersORM, RelProjectsWorkersORM.worker_id == WorkersORM.id)
        )

        workers_orm = (await session.execute(query)).all()

        workers = [WorkerByProjectDTO.model_validate(worker_orm, from_attributes=True) for worker_orm in workers_orm]

        await session.commit()
        return workers


async def get_plan_blocks_from_project(project_id: int) -> list[PlanBlockDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(PlanBlocksORM)
            .where(PlanBlocksORM.project_id == project_id)
        )

        plan_blocks_orm = (await session.execute(query)).scalars().all()
        plan_blocks = [PlanBlockDTO.model_validate(plan_block, from_attributes=True) for plan_block in plan_blocks_orm]

        await session.commit()
        return plan_blocks
