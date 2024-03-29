import datetime

from sqlalchemy import select, update, func, Sequence, insert
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql.functions import count

from database import Base, async_engine, async_session_factory
from models.workers import Workers
from models.projects import Projects, RelProjectsWorkers
from models.plan_blocks import PlanBlocks, BlockTesting, BlockBugs, PlanBlocksTransfer

from schemas.workers import WorkerDTO, WorkerAddDTO
from schemas.projects import ProjectAddDTO, ProjectDTO

from new_types import BugCategory, Level, SpecializationCode


async def add_worker(worker: WorkerAddDTO):
    session: AsyncSession
    async with async_session_factory() as session:
        worker_orm = Workers(
            **worker.dict()
        )

        session.add(worker_orm)

        await session.commit()


async def get_worker(worker_id: int) -> WorkerDTO:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(Workers).where(Workers.id == worker_id)
        )

        result = await session.execute(query)
        worker = result.scalars().all()[0]
        worker_dto = WorkerDTO.model_validate(worker, from_attributes=True)

        return worker_dto


async def fire_worker(worker_id: int) -> str:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            update(Workers)
            .where(Workers.id == worker_id)
            .values(fire_date=datetime.datetime.now(datetime.UTC)).returning(Workers.email)
        )

        result = await session.execute(query)
        await session.commit()

        print(f"RETURN EMAIL {result.scalar_one()=}")
        return result.scalar_one()


async def transfer_worker(worker_id: int, new_project_id: int, old_project_id: int | None):
    session: AsyncSession
    async with async_session_factory() as session:
        get_new_project_query = (
            select(Projects)
            .options(selectinload(Projects.workers))
            .filter_by(id=new_project_id)
        )
        get_worker_query = (
            select(Workers)
            .filter_by(id=worker_id)
        )

        new_project = (await session.execute(get_new_project_query)).scalar_one()
        worker = (await session.execute(get_worker_query)).scalar_one()

        new_project.workers.append(worker)

        if old_project_id is None:
            count_projects_query = (
                select(count()).select_from(RelProjectsWorkers)
                .where(
                    RelProjectsWorkers.worker_id == worker_id and
                    RelProjectsWorkers.project_hire_date is not None)
            )

            count_result = (await session.execute(count_projects_query)).first()[0]
            print(count_result)
            if count_result > 2:
                return

        else:
            # end_project_query = (
            #     update(RelProjectsWorkers)
            #     .where(
            #         RelProjectsWorkers.project_id == old_project_id and
            #         RelProjectsWorkers.worker_id == worker_id)
            #     .values(project_fire_date=datetime.datetime.now(datetime.UTC))
            # )
            #
            # await session.execute(end_project_query)
            get_old_project_query = (
                select(Projects)
                .options(selectinload(Projects.workers))
                .filter_by(id=old_project_id)
            )

            old_project = (await session.execute(get_old_project_query)).scalar_one()

            old_project.workers.remove(worker)

        # start_project_query = (
        #     insert(RelProjectsWorkers).values(worker_id=worker_id, project_id=new_project_id)
        # )
        #
        # await session.execute(start_project_query)

        await session.commit()
