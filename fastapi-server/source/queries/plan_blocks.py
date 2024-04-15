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
from new_types import SpecializationCode

from schemas.all import PlanBlockAddDTO

from schemas.plan_blocks import PlanBlockDTO, BlockBugAddDTO, BlockTestingDTO, BlockBugDTO, BlockWithTestAndBugs


async def get_plan_blocks(project_id: int) -> list[PlanBlockDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(PlanBlocksORM)
            .where(PlanBlocksORM.project_id == project_id)
            .group_by(PlanBlocksORM.id)
        )

        plan_blocks_orm = (await session.execute(query)).scalars().all()

        return [PlanBlockDTO.model_validate(plan_block, from_attributes=True) for plan_block in plan_blocks_orm]


async def get_plan_block(plan_block_id: int) -> PlanBlockDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(PlanBlocksORM)
            .where(PlanBlocksORM.id == plan_block_id)
        )

        plan_block_orm = (await session.execute(query)).scalar_one_or_none()

        return PlanBlockDTO.model_validate(plan_block_orm, from_attributes=True) if plan_block_orm else None


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

        query = (
            insert(PlanBlocksORM)
            .values(**plan_block.model_dump())
            .returning(PlanBlocksORM.id)
        )

        plan_block_id = (await session.execute(query)).scalar_one_or_none()

        await session.commit()
        return plan_block_id


async def close_plan_block(plan_block_id: int) -> BlockWithTestAndBugs | None:
    session: AsyncSession
    async with (async_session_factory() as session):
        query = (
            update(PlanBlocksORM)
            .where(PlanBlocksORM.id == plan_block_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(PlanBlocksORM)
            .options(selectinload(PlanBlocksORM.block_testing, PlanBlocksORM.block_bugs))
        )
        tests_close_query = (
            update(BlockTestingORM)
            .where(BlockTestingORM.block_id == plan_block_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
        )
        bugs_close_query = (
            update(BlockBugsORM)
            .where(BlockBugsORM.block_id == plan_block_id)
            .values(fix_date=datetime.datetime.now(datetime.UTC))
        )

        await session.execute(tests_close_query)
        await session.execute(bugs_close_query)
        plan_block_with_rel_orm = (await session.execute(query)).one_or_none()

        plan_block_dto = BlockWithTestAndBugs.model_validate(plan_block_with_rel_orm, from_attributes=True) \
            if plan_block_with_rel_orm else None

        await session.commit()
        return plan_block_dto


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

        #  Get plan block dates
        plan_block = await session.get(PlanBlocksORM, plan_block_id)
        if plan_block is None:
            return None
        plan_block_deadline: datetime.datetime = plan_block.deadline
        plan_block_start: datetime.datetime = plan_block.start_date
        plan_block_duration = plan_block_deadline - plan_block_start
        test_block_deadline = datetime.datetime.now(datetime.UTC) + plan_block_duration

        query = (
            insert(BlockTestingORM)
            .values(
                tester_id=tester_id,
                plan_block_id=plan_block_id,
                deadline=test_block_deadline
            )
            .returning(BlockTestingORM.id)
        )

        block_test_id = (await session.execute(query)).scalar_one_or_none()

        await session.commit()
        return block_test_id


async def close_block_test(block_test_id: int) -> BlockTestingDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(BlockTestingORM)
            .where(BlockTestingORM.id == block_test_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockTestingORM)
        )

        block_test_orm = (await session.execute(query)).scalars().first()
        block_test_dto = BlockTestingDTO.model_validate(block_test_orm, from_attributes=True) \
            if block_test_orm else None

        await session.commit()
        return block_test_dto


async def get_block_bugs(block_id: int) -> list[BlockBugDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(BlockBugsORM)
            .where(BlockBugsORM.block_id == block_id)
        )

        block_bugs_orm = (await session.execute(query)).scalars().all()
        block_bugs = [BlockBugDTO.model_validate(block_bug, from_attributes=True) for block_bug in block_bugs_orm]

        await session.commit()
        return block_bugs


async def add_block_bug(project_id: int, plan_block_id: int, block_bug: BlockBugAddDTO) -> int | None:
    session: AsyncSession
    async with async_session_factory() as session:
        # Check if block and tester are valid
        worker_check_query = (
            select(RelProjectsWorkersORM.worker_id)
            .where(
                and_(
                    RelProjectsWorkersORM.project_id == project_id,
                    RelProjectsWorkersORM.worker_id == block_bug.tester_id,
                    RelProjectsWorkersORM.project_fire_date == None
                )
            )
        )
        worker = await session.get(WorkersORM, block_bug.tester_id)
        if (worker is None) or (worker.specialization_code != SpecializationCode.tester) or \
                not (await session.execute(worker_check_query)).scalar_one_or_none():
            return None

        block_bug_deadline = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        query = (
            insert(BlockBugsORM)
            .values(
                **block_bug.model_dump(),
                block_id=plan_block_id,
                deadline=block_bug_deadline
            )
            .returning(BlockBugsORM.id)
        )

        block_bug_id = (await session.execute(query)).scalar_one_or_none()

        await session.commit()
        return block_bug_id


async def close_block_bug(block_bug_id: int) -> BlockBugDTO | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(BlockBugsORM)
            .where(BlockBugsORM.id == block_bug_id)
            .values(fix_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockBugsORM)
        )

        block_bug_orm = (await session.execute(query)).scalars().first()
        block_bug_dto = BlockBugDTO.model_validate(block_bug_orm, from_attributes=True) if block_bug_orm else None

        await session.commit()
        return block_bug_dto
