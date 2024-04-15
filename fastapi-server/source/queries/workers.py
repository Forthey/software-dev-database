import datetime

from sqlalchemy import select, update, insert, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from engine import async_session_factory
from models.workers import WorkersORM
from models.projects import ProjectsORM, RelProjectsWorkersORM
from models.plan_blocks import PlanBlocksORM, BlockTestingORM, BlockBugsORM, PlanBlocksTransferORM

from schemas.all import WorkerAddDTO, WorkerDTO, ProjectByWorkerDTO

from schemas.workers import WorkerOnFireDTO


async def get_workers() -> list[WorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
        )

        workers_orm = (await session.execute(query)).scalars().all()

        return [WorkerDTO.model_validate(worker_orm, from_attributes=True) for worker_orm in workers_orm]


async def get_worker(worker_id: int) -> WorkerDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        worker_orm = await session.get(WorkersORM, worker_id)

        return WorkerDTO.model_validate(worker_orm, from_attributes=True) if worker_orm else None


async def search_workers(username_mask: str) -> list[WorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
            .where(WorkersORM.username.icontains(username_mask))
        )

        workers_orm = (await session.execute(query)).scalars().all()

        return [WorkerDTO.model_validate(worker, from_attributes=True) for worker in workers_orm]


async def add_worker(worker: WorkerAddDTO) -> int | None:
    session: AsyncSession
    async with async_session_factory() as session:
        try:
            query = (
                insert(WorkersORM)
                .values(**worker.model_dump())
            )

            worker_id = (await session.execute(query)).scalar_one()

            await session.commit()
            return worker_id
        except IntegrityError:
            return None


async def fire_worker(worker_id: int, fire_reason: str) -> WorkerOnFireDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(WorkersORM)
            .where(WorkersORM.id == worker_id)
            .values(
                fire_date=datetime.datetime.now(datetime.UTC),
                fire_reason=fire_reason
            )
            .returning(WorkersORM)
        )

        worker_orm = (await session.execute(query)).scalar_one_or_none()
        if worker_orm is None:
            return None
        worker = WorkerDTO.model_validate(worker_orm, from_attributes=True)

        plan_blocks_query = (
            update(PlanBlocksORM)
            .where(PlanBlocksORM.developer_id == worker_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(PlanBlocksORM.id)
        )

        plan_blocks_id = (await session.execute(plan_blocks_query)).scalars().all()

        projects_query = (
            update(RelProjectsWorkersORM)
            .where(RelProjectsWorkersORM.worker_id == worker_id)
            .values(project_fire_date=datetime.datetime.now(datetime.UTC))
            .returning(RelProjectsWorkersORM.project_id)
        )
        block_testing_query = (
            update(BlockTestingORM)
            .where(BlockTestingORM.block_id.in_(plan_blocks_id))
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockTestingORM.id)
        )
        block_bugs_query = (
            update(BlockBugsORM)
            .where(BlockBugsORM.block_id.in_(plan_blocks_id))
        )

        projects_id = (await session.execute(projects_query)).scalars().all()
        block_testings_id = (await session.execute(block_testing_query)).scalars().all()
        block_bugs_id = (await session.execute(block_bugs_query)).scalars().all()

        await session.commit()
        return WorkerOnFireDTO(
            **worker.model_dump(),
            projects_id=projects_id,
            plan_blocks_id=plan_blocks_id,
            block_testings_id=block_testings_id,
            block_bugs_id=block_bugs_id
        )


async def add_overdue(worker_id: int) -> WorkerOnFireDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(WorkersORM)
            .where(WorkersORM.id == worker_id)
            .values(WorkersORM.overdue_count+1)
            .returning(WorkersORM)
        )

        worker = (await session.execute(query)).scalars().first()

        if worker is None or worker.overdue_count < 7:
            await session.commit()
            return None

        await session.commit()
        return await fire_worker(worker_id, "Число просрочек превысило допустимый лимит")


async def fire_due_to_overdue() -> list[WorkerOnFireDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        workers: list[WorkerOnFireDTO] = []

        query = (
            select(WorkersORM.id)
            .where(WorkersORM.overdue_count >= 7)
        )

        workers_id = (await session.execute(query)).scalars().all()
        for worker_id in workers_id:
            workers.append(await fire_worker(worker_id, "Число просрочек превысило допустимый лимит"))

        await session.commit()
        return workers


async def get_projects_from_worker(worker_id: int) -> list[ProjectByWorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        projects_query = (
            select(ProjectsORM.__table__.columns,
                   RelProjectsWorkersORM.project_hire_date,
                   RelProjectsWorkersORM.project_fire_date)
            .select_from(RelProjectsWorkersORM)
            .where(
                and_(
                    RelProjectsWorkersORM.worker_id == worker_id,
                    RelProjectsWorkersORM.project_fire_date is None
                )
            )
            .join(ProjectsORM, RelProjectsWorkersORM.project_id == ProjectsORM.id)
        )

        projects_orm = (await session.execute(projects_query)).all()

        workers_dto = [ProjectByWorkerDTO.model_validate(project_orm, from_attributes=True)
                       for project_orm in projects_orm]

        await session.commit()
        return workers_dto


async def transfer_worker(worker_id: int, new_project_id: int, old_project_id: int | None) -> bool:
    session: AsyncSession
    async with async_session_factory() as session:
        get_new_project_query = (
            select(ProjectsORM)
            .options(selectinload(ProjectsORM.workers))
            .where(
                and_(
                    ProjectsORM.id == new_project_id,
                    ProjectsORM.end_date is None
                )
            )
        )
        get_worker_query = (
            select(WorkersORM)
            .where(
                and_(
                    WorkersORM.id == worker_id,
                    WorkersORM.fire_date is None
                )
            )
        )

        new_project = (await session.execute(get_new_project_query)).scalar_one_or_none()
        worker = (await session.execute(get_worker_query)).scalar_one_or_none()

        if new_project is None or worker is None:
            return False

        new_project.workers.append(worker)

        if old_project_id is None:
            count_projects_query = (
                select(count()).select_from(RelProjectsWorkersORM)
                .where(
                    and_(
                        RelProjectsWorkersORM.worker_id == worker_id,
                        RelProjectsWorkersORM.project_fire_date is None
                    )
                )
            )

            count_result = (await session.execute(count_projects_query)).scalar_one()
            print(count_result)

            if count_result > 2:
                return False

        else:
            end_project_query = (
                update(RelProjectsWorkersORM)
                .where(and_(
                    RelProjectsWorkersORM.project_id == int(old_project_id),
                    RelProjectsWorkersORM.worker_id == worker_id),
                    RelProjectsWorkersORM.project_fire_date is None
                )
                .values(project_fire_date=datetime.datetime.now(datetime.UTC))
                .returning(ProjectsORM.id)
            )

            old_project_id = (await session.execute(end_project_query)).scalar_one_or_none()

            if old_project_id is None:
                return False

        await session.commit()
        return True
