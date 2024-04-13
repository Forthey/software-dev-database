import datetime

from sqlalchemy import select, func, Sequence, update
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

from schemas.all import PlanBlockAddDTO

from schemas.plan_blocks import PlanBlockDTO, BlockBugAddDTO, BlockTestingDTO, BlockBugDTO


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


async def add_plan_block(plan_block: PlanBlockAddDTO) -> None:
    session: AsyncSession
    async with async_session_factory() as session:
        plan_block_orm = PlanBlocksORM(**plan_block.model_dump())
        session.add(plan_block_orm)

        await session.commit()


async def close_plan_block(plan_block_id: int) -> datetime.datetime | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(PlanBlocksORM)
            .where(PlanBlocksORM.id == plan_block_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(PlanBlocksORM.deadline)
        )

        deadline = (await session.execute(query)).scalar_one_or_none()

        await session.commit()
        return deadline


async def get_block_tests(block_id: int) -> list[BlockTestingDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(BlockTestingORM)
            .where(BlockTestingORM.block_id == block_id)
        )

        block_tests_orm = (await session.execute(query)).scalars().all()

        return [BlockTestingDTO.model_validate(block_test, from_attributes=True) for block_test in block_tests_orm]


async def send_block_to_test(plan_block_id: int, tester_id: int) -> None:
    session: AsyncSession
    async with async_session_factory() as session:
        block_test_orm = BlockTestingORM(tester_id=tester_id, plan_block_id=plan_block_id)
        session.add(block_test_orm)

        await session.commit()


async def close_block_test(block_test_id: int) -> datetime.datetime | None:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(BlockTestingORM)
            .where(BlockTestingORM.id == block_test_id)
            .values(end_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockTestingORM.deadline)
        )

        result = (await session.execute(query)).scalar_one_or_none()

        await session.commit()
        return result


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


async def add_block_bugs(block_bugs: list[BlockBugAddDTO]) -> None:
    session: AsyncSession
    async with async_session_factory() as session:
        block_bugs_orm = [BlockBugsORM(**block_bug.model_dump()) for block_bug in block_bugs]
        session.add(block_bugs_orm)

        await session.commit()


async def close_block_bug(block_bug_id: int) -> datetime.datetime | None:
    session: AsyncSession
    async with async_session_factory()as session:
        query = (
            update(BlockBugsORM)
            .where(BlockBugsORM.id == block_bug_id)
            .values(fix_date=datetime.datetime.now(datetime.UTC))
            .returning(BlockBugsORM.detection_date)
        )

        result = (await session.execute(query)).scalar_one_or_none()

        await session.commit()
        return result
