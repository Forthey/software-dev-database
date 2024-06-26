import datetime

from sqlalchemy import select, update, and_
from sqlalchemy.dialects.postgresql import insert
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
from new_types import SpecializationCode
from queries.plan_blocks import close_plan_blocks

from schemas.all import WorkerAddDTO, WorkerDTO, ProjectByWorkerDTO
from schemas.plan_blocks import PlanBlockDTO

from schemas.workers import WorkerOnFireDTO


async def get_workers(spec_code: SpecializationCode | None = None) -> list[WorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
        )
        if spec_code:
            query = query.where(WorkersORM.specialization_code == spec_code)

        workers_orm = (await session.execute(query)).scalars().all()

        return [WorkerDTO.model_validate(worker_orm, from_attributes=True) for worker_orm in workers_orm]


async def get_worker(worker_id: int) -> WorkerDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        worker_orm = await session.get(WorkersORM, worker_id)

        return WorkerDTO.model_validate(worker_orm, from_attributes=True) if worker_orm else None


async def search_workers(username_mask: str, spec_code: SpecializationCode | None = None) -> list[WorkerDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
            .where(WorkersORM.username.icontains(username_mask))
        )
        if spec_code:
            query = query.where(WorkersORM.specialization_code == spec_code)

        workers_orm = (await session.execute(query)).scalars().all()

        return [WorkerDTO.model_validate(worker, from_attributes=True) for worker in workers_orm]


async def add_worker(worker: WorkerAddDTO) -> int | None:
    session: AsyncSession
    async with async_session_factory() as session:
        try:
            query = (
                insert(WorkersORM)
                .values(**worker.model_dump())
                .returning(WorkersORM.id)
            )

            worker_id = (await session.execute(query)).scalar_one()

            await session.commit()
            return worker_id
        except IntegrityError:
            return None


async def restore_worker(worker_id: int) -> WorkerDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(WorkersORM)
            .where(
                and_(
                    WorkersORM.id == worker_id,
                    WorkersORM.fire_date != None
                )
            )
            .values(
                fire_date=None
            )
            .returning(WorkersORM)
        )

        worker_orm = (await session.execute(query)).scalar_one_or_none()
        worker = WorkerDTO.model_validate(worker_orm, from_attributes=True) if worker_orm else None

        await session.commit()
        return worker


async def fire_worker(worker_id: int, fire_reason: str) -> WorkerOnFireDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        # Set worker fire info
        query = (
            update(WorkersORM)
            .where(
                and_(
                    WorkersORM.id == worker_id,
                    WorkersORM.fire_date == None
                )
            )
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

        # Fire worker from all projects
        projects_query = (
            update(RelProjectsWorkersORM)
            .where(
                and_(
                    RelProjectsWorkersORM.worker_id == worker_id,
                    RelProjectsWorkersORM.project_fire_date == None
                )
            )
            .values(project_fire_date=datetime.datetime.now(datetime.UTC))
            .returning(RelProjectsWorkersORM.project_id)
        )

        if worker.specialization_code == SpecializationCode.developer:
            # Select all plan blocks related to developer
            plan_blocks_query = (
                select(PlanBlocksORM.id)
                .where(
                    and_(
                        PlanBlocksORM.developer_id == worker_id,
                        PlanBlocksORM.end_date == None
                    )
                )
            )

            plan_blocks_id = (await session.execute(plan_blocks_query)).scalars().all()
            # Close all plan blocks
            await close_plan_blocks(list(map(int, plan_blocks_id)))
        else:
            # Close all block test and bugs related to tester
            block_testing_query = (
                update(BlockTestingORM)
                .where(
                    and_(
                        BlockTestingORM.tester_id == worker_id,
                        BlockTestingORM.end_date == None
                    )
                )
                .values(end_date=datetime.datetime.now(datetime.UTC))
                .returning(BlockTestingORM.id)
            )
            block_bugs_query = (
                update(BlockBugsORM)
                .where(
                    and_(
                        BlockBugsORM.tester_id == worker_id,
                        BlockBugsORM.fix_date == None
                    )
                )
            )
            block_testings_id = (await session.execute(block_testing_query)).scalars().all()
            block_bugs_id = (await session.execute(block_bugs_query)).scalars().all()

        projects_id = (await session.execute(projects_query)).scalars().all()

        await session.commit()
        return WorkerOnFireDTO(
            **worker.model_dump(),
            projects_id=projects_id,
        )


async def fire_worker_from_project(project_id: int, worker_id: int) -> bool:
    session = AsyncSession
    async with async_session_factory() as session:
        # Fire worker from project
        query = (
            update(RelProjectsWorkersORM)
            .where(
                and_(
                    RelProjectsWorkersORM.worker_id == worker_id,
                    RelProjectsWorkersORM.project_id == project_id,
                    RelProjectsWorkersORM.project_fire_date == None
                )
            )
            .values(project_fire_date=datetime.datetime.now(datetime.UTC))
            .returning(RelProjectsWorkersORM.project_id)
        )

        project_id = (await session.execute(query)).scalar_one_or_none()

        if project_id is None:
            return False

        # Select all plan blocks related to developer in project
        plan_blocks_query = (
            select(PlanBlocksORM.id)
            .where(
                and_(
                    PlanBlocksORM.developer_id == worker_id,
                    PlanBlocksORM.project_id == project_id,
                    PlanBlocksORM.end_date == None
                )
            )
        )

        plan_blocks_id = (await session.execute(plan_blocks_query)).scalars().all()
        # Close all plan blocks
        await close_plan_blocks(list(map(int, plan_blocks_id)))

        # Close all block test and bugs related to tester and project
        block_testing_query = (
            update(BlockTestingORM)
            .where(
                and_(
                    BlockTestingORM.tester_id == worker_id,
                    BlockTestingORM.block_id.in_(plan_blocks_id),
                    BlockTestingORM.end_date == None
                )
            )
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockTestingORM.id)
        )
        block_bugs_query = (
            update(BlockBugsORM)
            .where(
                and_(
                    BlockBugsORM.tester_id == worker_id,
                    BlockBugsORM.block_id.in_(plan_blocks_id),
                    BlockBugsORM.fix_date == None
                )
            )
            .values(fix_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockBugsORM.id)
        )
        block_testings_id = (await session.execute(block_testing_query)).scalars().all()
        block_bugs_id = (await session.execute(block_bugs_query)).scalars().all()

        await session.commit()
        return True


async def add_overdue(worker_id: int) -> WorkerOnFireDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(WorkersORM)
            .where(WorkersORM.id == worker_id)
            .values(overdue_count=WorkersORM.overdue_count+1)
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
            .where(
                and_(
                    WorkersORM.overdue_count >= 7,
                    WorkersORM.fire_date == None
                )
            )
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
            .where(RelProjectsWorkersORM.worker_id == worker_id)
            .join(ProjectsORM, RelProjectsWorkersORM.project_id == ProjectsORM.id)
        )

        projects_orm = (await session.execute(projects_query)).all()

        return [ProjectByWorkerDTO.model_validate(project_orm, from_attributes=True) for project_orm in projects_orm]


async def transfer_worker(worker_id: int, new_project_id: int, old_project_id: int | None) -> bool:
    session: AsyncSession
    async with async_session_factory() as session:
        get_new_project_query = (
            select(ProjectsORM)
            .options(selectinload(ProjectsORM.workers))
            .where(
                and_(
                    ProjectsORM.id == new_project_id,
                    ProjectsORM.end_date == None
                )
            )
        )
        get_worker_query = (
            select(WorkersORM)
            .where(
                and_(
                    WorkersORM.id == worker_id,
                    WorkersORM.fire_date == None
                )
            )
        )

        new_project = (await session.execute(get_new_project_query)).scalar_one_or_none()
        worker = (await session.execute(get_worker_query)).scalar_one_or_none()

        if new_project is None or worker is None:
            return False

        try:
            insert_query = (
                insert(RelProjectsWorkersORM)
                .values(
                    worker_id=worker_id,
                    project_id=new_project_id,
                    project_fire_date=None
                )
            ).on_conflict_do_update(
                index_elements=[RelProjectsWorkersORM.worker_id, RelProjectsWorkersORM.project_id],
                set_=dict(
                    worker_id=worker_id,
                    project_id=new_project_id,
                    project_fire_date=None
                )
            )

            await session.execute(insert_query)
        except IntegrityError as e:
            print("Cringe")

        if old_project_id is None:
            count_projects_query = (
                select(count()).select_from(RelProjectsWorkersORM)
                .where(
                    and_(
                        RelProjectsWorkersORM.worker_id == worker_id,
                        RelProjectsWorkersORM.project_fire_date == None
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
                    RelProjectsWorkersORM.project_fire_date == None
                )
                .values(project_fire_date=datetime.datetime.now(datetime.UTC))
                .returning(ProjectsORM.id)
            )

            old_project_id = (await session.execute(end_project_query)).scalar_one_or_none()

            if old_project_id is None:
                return False

        await session.commit()
        return True


async def get_plan_blocks(worker_id: int) -> list[PlanBlockDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(
                PlanBlocksORM.__table__.columns,
                PlanBlocksTransferORM.new_status.label("status"),
                PlanBlocksTransferORM.date.label("status_date")
            )
            .select_from(PlanBlocksORM)
            .where(PlanBlocksORM.developer_id == worker_id)
            .join(PlanBlocksTransferORM, PlanBlocksTransferORM.block_id == PlanBlocksORM.id)
            .order_by(PlanBlocksORM.id, PlanBlocksTransferORM.date.desc())
        )

        plan_blocks_orm = (await session.execute(query)).unique().all()

        print(plan_blocks_orm)

        return [PlanBlockDTO.model_validate(plan_block, from_attributes=True) for plan_block in plan_blocks_orm]
