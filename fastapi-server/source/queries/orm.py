from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, async_engine, async_session_factory
from db_models.models import Workers, Projects, PlanBlocks, PlanBlocksTransfer, BlockTesting, BlockBugs


class AsyncORM:
    """
    TODO: RE DESCRIBE FUNCTIONS, BECAUSE I TRIED TO MAKE PROGRAM LOGIC IN ORM
    THESE FUNCTIONS SHOULD BE IN SERVER (PROGRAM) LOGIC, IN THIS CLASS ONLY QUERIES
    """

    #
    # Table creating
    #

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    #
    # Workers management
    #

    @staticmethod
    async def add_new_worker(worker: Workers):
        session: AsyncSession
        async with async_session_factory() as session:
            session.add(worker)
            await session.commit()

    # TODO: this function
    @staticmethod
    async def transfer_worker_between_projects(worker_id: int,
                                               new_project_id: int,
                                               old_project_id: int | None):
        ...

    #
    # Project management
    #

    # TODO: this function
    @staticmethod
    async def close_project(project_id: int):
        ...

    # TODO: this function
    @staticmethod
    async def start_project(project: Projects,
                            workers_id: list[int] | None,
                            developers_id: list[int] | None,
                            testers_id: list[int] | None):
        ...

    @staticmethod
    async def get_plan_blocks(project_id: int) -> tuple[PlanBlocks]:
        session: AsyncSession
        with async_session_factory() as session:
            # TODO: I'll leave it here for a while, mask %thing%
            # PlanBlocks.development_id.contains("thing")
            query = (
                select(PlanBlocks)
                .where(PlanBlocks.development_id == project_id)
                .group_by(PlanBlocks.id)
            )
            result = await session.execute(query)
            plan_blocks = result.tuples().all()[0]
            await session.commit()
            return plan_blocks

    @staticmethod
    async def update_project_description(project_id: int, description: str) -> bool:
        with async_session_factory() as session:
            # TODO: maybe should be changed to basic update to reduce amount of queries
            project = await session.get(Projects, project_id)
            if project is None:
                return False
            project.description = description
            session.commit()

        return True
    #
    # Block info
    #

    # TODO: this function
    @staticmethod
    async def get_block_transfer(block_id: int) -> list[PlanBlocksTransfer]:
        ...

    # TODO: this function
    @staticmethod
    async def get_block_tests(block_id: int) -> list[BlockTesting]:
        ...

    # TODO: this function
    @staticmethod
    async def get_block_bugs(block_id: int) -> list[BlockBugs]:
        ...

    #
    # Overdue
    #

    # TODO: this function
    @staticmethod
    async def fetch_all_overdue() -> list[Workers]:
        ...

    # TODO: this function
    @staticmethod
    async def fire_workers_for_overdue() -> list[Workers]:
        ...

    # TODO: this function
    @staticmethod
    async def get_project_blocks_overdue(project_id: int) -> list[PlanBlocks]:
        ...

    # TODO: this function
    @staticmethod
    async def get_project_tests_overdue(project_id: int) -> list[BlockTesting]:
        ...

    # TODO: this function
    @staticmethod
    async def get_project_bugs_overdue(project_id: int) -> list[BlockBugs]:
        ...

    #
    # Reports
    #

    # TODO: describe and implement other functions
    # TODO: restructure functions
