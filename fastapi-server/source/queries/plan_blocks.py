import datetime

from sqlalchemy import select, func, Sequence, update, and_, insert
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
from new_types import SpecializationCode, BlockStatus

from schemas.all import PlanBlockAddDTO

from schemas.plan_blocks import PlanBlockDTO, BlockBugAddDTO, BlockTestingDTO, BlockBugDTO, BlockWithTestAndBugs
from schemas.workers import WorkerDTO


async def get_plan_blocks(project_id: int) -> list[PlanBlockDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(
                PlanBlocksORM.__table__.columns,
                PlanBlocksTransferORM.new_status.label("status"),
                PlanBlocksTransferORM.date.label("status_date")
            )
            .distinct(PlanBlocksORM.id)
            .where(PlanBlocksORM.project_id == project_id)
            .join(PlanBlocksTransferORM, PlanBlocksTransferORM.block_id == PlanBlocksORM.id)
            .order_by(PlanBlocksORM.id, PlanBlocksTransferORM.date.desc())
        )

        plan_blocks_orm = (await session.execute(query)).all()

        return [PlanBlockDTO.model_validate(plan_block, from_attributes=True) for plan_block in plan_blocks_orm]


async def get_plan_block(plan_block_id: int) -> PlanBlockDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(
                PlanBlocksORM.__table__.columns,
                PlanBlocksTransferORM.new_status.label("status"),
                PlanBlocksTransferORM.date.label("status_date")
            )
            .where(PlanBlocksORM.id == plan_block_id)
            .join(PlanBlocksTransferORM, PlanBlocksTransferORM.block_id == PlanBlocksORM.id)
            .order_by(PlanBlocksTransferORM.date.desc())
            .limit(1)
        )

        plan_block_orm = (await session.execute(query)).one_or_none()

        print(plan_block_orm)

        return PlanBlockDTO.model_validate(plan_block_orm, from_attributes=True) if plan_block_orm else None


async def get_plan_block_tester(plan_block_id: int) -> WorkerDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(WorkersORM)
            .where(WorkersORM.id.in_(
                select(PlanBlocksTransferORM.tester_id)
                .where(PlanBlocksTransferORM.block_id == plan_block_id)
                .order_by(PlanBlocksTransferORM.id.desc())
                .limit(1)
            ))
        )

        worker_orm = (await session.execute(query)).scalar_one_or_none()

        return WorkerDTO.model_validate(worker_orm, from_attributes=True) if worker_orm else None


async def add_plan_block(plan_block: PlanBlockAddDTO) -> int | None:
    session: AsyncSession
    async with (async_session_factory() as session):
        # Check if worker is in project and he is developer
        worker_check_query = (
            select(RelProjectsWorkersORM.worker_id)
            .where(
                and_(
                    RelProjectsWorkersORM.project_id == plan_block.project_id,
                    RelProjectsWorkersORM.worker_id == plan_block.developer_id,
                    RelProjectsWorkersORM.project_fire_date == None
                )
            )
        )
        worker = await session.get(WorkersORM, plan_block.developer_id)
        if (worker is None) or (worker.specialization_code != SpecializationCode.developer) or \
                not (await session.execute(worker_check_query)).scalar_one_or_none():
            return None

        # Add plan block
        query = (
            insert(PlanBlocksORM)
            .values(**plan_block.model_dump())
            .returning(PlanBlocksORM.id)
        )

        plan_block_id = (await session.execute(query)).scalar_one_or_none()

        # Set plan block status "in progress"
        transfer_query = (
            insert(PlanBlocksTransferORM)
            .values(
                block_id=plan_block_id,
                new_status=BlockStatus.in_progress,
            )
        )

        await session.execute(transfer_query)

        await session.commit()
        return plan_block_id


async def close_plan_block(plan_block_id: int) -> BlockWithTestAndBugs | None:
    session: AsyncSession
    async with (async_session_factory() as session):
        query = (
            update(PlanBlocksORM)
            .where(
                and_(
                    PlanBlocksORM.id == plan_block_id,
                    PlanBlocksORM.end_date == None
                )
            )
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(PlanBlocksORM)
            .options(selectinload(PlanBlocksORM.block_testing), selectinload(PlanBlocksORM.block_bugs))
        )

        plan_block_with_rel_orm = (await session.execute(query)).scalar_one_or_none()

        if plan_block_with_rel_orm is None:
            return None

        tests_close_query = (
            update(BlockTestingORM)
            .where(
                and_(
                    BlockTestingORM.block_id == plan_block_id,
                    BlockTestingORM.end_date == None
                )
            )
            .values(end_date=datetime.datetime.now(datetime.UTC))
        )
        bugs_close_query = (
            update(BlockBugsORM)
            .where(
                and_(
                    BlockBugsORM.block_id == plan_block_id,
                    BlockBugsORM.fix_date == None
                )
            )
            .values(fix_date=datetime.datetime.now(datetime.UTC))
        )
        plan_blocks_transfer_query = (
            insert(PlanBlocksTransferORM)
            .values(new_status=BlockStatus.completed, block_id=plan_block_id)
        )

        await session.execute(tests_close_query)
        await session.execute(bugs_close_query)
        await session.execute(plan_blocks_transfer_query)

        plan_block_dto = BlockWithTestAndBugs.model_validate(plan_block_with_rel_orm, from_attributes=True) \
            if plan_block_with_rel_orm else None

        await session.commit()
        return plan_block_dto


async def close_plan_blocks(plan_blocks_id: list[int]) -> list[BlockWithTestAndBugs]:
    async with async_session_factory() as session:
        # Close plan blocks
        query = (
            update(PlanBlocksORM)
            .where(PlanBlocksORM.id.in_(plan_blocks_id))
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(PlanBlocksORM)
            .options(selectinload(PlanBlocksORM.block_testing), selectinload(PlanBlocksORM.block_bugs))
        )
        # Close plan blocks tests
        tests_close_query = (
            update(BlockTestingORM)
            .where(BlockTestingORM.block_id.in_(plan_blocks_id))
            .values(end_date=datetime.datetime.now(datetime.UTC))
        )
        # Close plan blocks bugs
        bugs_close_query = (
            update(BlockBugsORM)
            .where(BlockBugsORM.block_id.in_(plan_blocks_id))
            .values(fix_date=datetime.datetime.now(datetime.UTC))
        )

        for block_id in plan_blocks_id:
            session.add(PlanBlocksTransferORM(new_status=BlockStatus.completed, block_id=block_id))

        plan_blocks_orm = (await session.execute(query)).scalars().all()
        await session.execute(tests_close_query)
        await session.execute(bugs_close_query)
        # await session.execute(plan_blocks_transfer_query)

        plan_blocks = [BlockWithTestAndBugs.model_validate(plan_block, from_attributes=True)
                       for plan_block in plan_blocks_orm]

        await session.commit()
        return plan_blocks


async def get_block_tests(block_id: int) -> list[BlockTestingDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(BlockTestingORM)
            .where(BlockTestingORM.block_id == block_id)
        )

        block_tests_orm = (await session.execute(query)).scalars().all()

        return [BlockTestingDTO.model_validate(block_test, from_attributes=True) for block_test in block_tests_orm]


async def send_block_to_test(project_id: int, plan_block_id: int, tester_id: int) -> int | None:
    session: AsyncSession
    async with async_session_factory() as session:
        # Check if worker is in project and he is tester
        worker_check_query = (
            select(RelProjectsWorkersORM.worker_id)
            .where(
                and_(
                    RelProjectsWorkersORM.project_id == project_id,
                    RelProjectsWorkersORM.worker_id == tester_id,
                    RelProjectsWorkersORM.project_fire_date == None
                )
            )
        )
        worker = await session.get(WorkersORM, tester_id)
        if (worker is None) or (worker.specialization_code != SpecializationCode.tester) or \
                not (await session.execute(worker_check_query)).scalar_one_or_none():
            return None

        #  Get plan block dates to eval test block deadline
        plan_block = await session.get(PlanBlocksORM, plan_block_id)
        if plan_block is None:
            return None
        plan_block_deadline: datetime.datetime = plan_block.deadline
        plan_block_start: datetime.datetime = plan_block.start_date
        plan_block_duration = plan_block_deadline - plan_block_start
        test_block_deadline = datetime.datetime.now(datetime.UTC) + plan_block_duration

        # Add block test
        query = (
            insert(BlockTestingORM)
            .values(
                tester_id=tester_id,
                block_id=plan_block_id,
                deadline=test_block_deadline
            )
            .returning(BlockTestingORM.id)
        )

        block_test_id = (await session.execute(query)).scalar_one_or_none()

        # Add transfer info for block
        transfer_query = (
            insert(PlanBlocksTransferORM)
            .values(
                block_id=plan_block_id,
                new_status=BlockStatus.on_testing,
                tester_id=tester_id
            )
        )

        await session.execute(transfer_query)

        await session.commit()
        return block_test_id


async def close_block_test(block_test_id: int) -> BlockTestingDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        # Close test
        query = (
            update(BlockTestingORM)
            .where(
                and_(
                    BlockTestingORM.id == block_test_id,
                    BlockTestingORM.end_date == None
                )
            )
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockTestingORM)
        )

        block_test_orm = (await session.execute(query)).scalars().first()

        if block_test_orm is None:
            return None

        # Add transfer info for block
        transfer_query = (
            insert(PlanBlocksTransferORM)
            .values(
                block_id=block_test_orm.block_id,
                new_status=BlockStatus.in_progress,
                tester_id=block_test_orm.tester_id
            )
        )

        await session.execute(transfer_query)

        block_test_dto = BlockTestingDTO.model_validate(block_test_orm, from_attributes=True)

        await session.commit()
        return block_test_dto


async def get_block_bugs(block_id: int) -> list[BlockBugDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(BlockBugsORM)
            .where(
                and_(
                    BlockBugsORM.block_id == block_id,
                    BlockBugsORM.fix_date == None
                )
            )
        )

        block_bugs_orm = (await session.execute(query)).scalars().all()
        block_bugs = [BlockBugDTO.model_validate(block_bug, from_attributes=True) for block_bug in block_bugs_orm]

        await session.commit()
        return block_bugs


async def add_block_bugs(project_id: int, plan_block_id: int, tester_id,
                         block_bugs: list[BlockBugAddDTO]) -> list[int] | None:
    session: AsyncSession
    async with async_session_factory() as session:
        # Check if block and tester are valid
        worker_check_query = (
            select(RelProjectsWorkersORM.worker_id)
            .where(
                and_(
                    RelProjectsWorkersORM.project_id == project_id,
                    RelProjectsWorkersORM.worker_id == tester_id,
                    RelProjectsWorkersORM.project_fire_date == None
                )
            )
        )
        worker = await session.get(WorkersORM, tester_id)
        if (worker is None) or (worker.specialization_code != SpecializationCode.tester) or \
                not (await session.execute(worker_check_query)).scalar_one_or_none():
            return None

        block_bug_deadline = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        # Add bugs

        for block_bug in block_bugs:
            session.add(BlockBugsORM(
                title=block_bug.title,
                category=block_bug.category,
                block_id=plan_block_id,
                tester_id=tester_id,
                deadline=block_bug_deadline))

        await session.flush()

        # Change block state
        transfer_query = (
            insert(PlanBlocksTransferORM)
            .values(
                block_id=plan_block_id,
                new_status=BlockStatus.in_progress,
                tester_id=tester_id,
            )
        )

        await session.execute(transfer_query)

        await session.commit()
        return [1]


async def close_block_bug(block_bug_id: int) -> BlockBugDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(BlockBugsORM)
            .where(
                and_(
                    BlockBugsORM.id == block_bug_id,
                    BlockBugsORM.fix_date == None
                )
            )
            .values(fix_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockBugsORM)
        )

        block_bug_orm = (await session.execute(query)).scalars().first()
        block_bug_dto = BlockBugDTO.model_validate(block_bug_orm, from_attributes=True) if block_bug_orm else None

        await session.commit()
        return block_bug_dto
