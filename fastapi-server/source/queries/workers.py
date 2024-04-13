import datetime

from sqlalchemy import select, update, func, Sequence, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql.functions import count

from engine import async_session_factory
from models.workers import WorkersORM
from models.projects import ProjectsORM, RelProjectsWorkersORM
from models.plan_blocks import PlanBlocksORM, BlockTestingORM, BlockBugsORM, PlanBlocksTransferORM

from schemas.all import WorkerAddDTO, WorkerDTO, ProjectByWorkerDTO

from new_types import BugCategory, Level, SpecializationCode, ResultInfo


async def get_workers() -> list[WorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
        )

        workers_orm = (await session.execute(query)).scalars().all()

        return [WorkerDTO.model_validate(worker_orm, from_attributes=True) for worker_orm in workers_orm]


async def get_worker(worker_id: int) -> WorkerDTO:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM).where(WorkersORM.id == worker_id)
        )

        result = await session.execute(query)
        worker = result.scalar_one_or_none()

        return WorkerDTO.model_validate(worker, from_attributes=True)


async def search_workers(username_mask: str) -> list[WorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
            .where(WorkersORM.username.icontains(username_mask))
        )

        workers_orm = (await session.execute(query)).scalars().all()

        return [WorkerDTO.model_validate(worker, from_attributes=True) for worker in workers_orm]


async def add_worker(worker: WorkerAddDTO) -> ResultInfo:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
            .where(worker.username == WorkersORM.username)
        )

        if (await session.execute(query)).all():
            await session.commit()
            return ResultInfo.failure

        worker_orm = WorkersORM(
            **worker.dict()
        )

        session.add(worker_orm)

        await session.commit()

        return ResultInfo.success


# TODO возвращать работника и писать ему письмо о том, что он уволен
async def fire_worker(worker_id: int) -> ResultInfo:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(WorkersORM)
            .where(WorkersORM.id == worker_id)
            .values(fire_date=datetime.datetime.now(datetime.UTC))
            .returning(WorkersORM)
        )

        result = await session.execute(query)
        await session.commit()

        if not result.all():
            return ResultInfo.failure

        return ResultInfo.success


async def fire_due_to_overdue() -> list[WorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(WorkersORM)
            .where(WorkersORM.overdue_count > 7)
            .values(fire_date=datetime.datetime.now(datetime.UTC))
            .returning(WorkersORM)
        )

        result_workers = (await session.execute(query)).scalars().all()
        await session.commit()

        return [WorkerDTO.model_validate(worker, from_attributes=True) for worker in result_workers]


async def get_projects_from_worker(worker_id: int) -> list[ProjectByWorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        projects_query = (
            select(ProjectsORM.__table__.columns,
                   RelProjectsWorkersORM.project_hire_date,
                   RelProjectsWorkersORM.project_fire_date)
            .select_from(RelProjectsWorkersORM)
            .where(RelProjectsWorkersORM.worker_id == worker_id and RelProjectsWorkersORM.project_fire_date == None)
            .join(ProjectsORM, RelProjectsWorkersORM.project_id == ProjectsORM.id)
        )

        result = await session.execute(projects_query)

        projects_orm = result.all()

        print(f"{projects_orm=}")
        workers_dto = [ProjectByWorkerDTO.model_validate(project_orm, from_attributes=True) for project_orm in
                       projects_orm]

        await session.commit()

        return workers_dto


async def transfer_worker(worker_id: int, new_project_id: int, old_project_id: int | None) -> bool:
    session: AsyncSession
    async with async_session_factory() as session:
        get_new_project_query = (
            select(ProjectsORM)
            .options(selectinload(ProjectsORM.workers))
            .filter_by(id=new_project_id)
        )
        get_worker_query = (
            select(WorkersORM)
            .filter_by(id=worker_id)
        )

        new_project = (await session.execute(get_new_project_query)).scalar_one()
        worker = (await session.execute(get_worker_query)).scalar_one()

        new_project.workers.append(worker)

        if old_project_id is None:
            count_projects_query = (
                select(count()).select_from(RelProjectsWorkersORM)
                .where(
                    RelProjectsWorkersORM.worker_id == worker_id and
                    RelProjectsWorkersORM.project_hire_date is not None)
            )

            count_result = (await session.execute(count_projects_query)).scalar_one()
            print(count_result)
            if count_result > 2:
                return False

        else:
            end_project_query = (
                update(RelProjectsWorkersORM)
                .where(and_(RelProjectsWorkersORM.project_id == int(old_project_id),
                            RelProjectsWorkersORM.worker_id == worker_id))
                .values(project_fire_date=datetime.datetime.now(datetime.UTC))
            )

            await session.execute(end_project_query)

        await session.commit()
        return True
