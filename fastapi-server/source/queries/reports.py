import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from engine import async_session_factory
from models.plan_blocks import PlanBlocksORM
from models.projects import ProjectsORM, RelProjectsWorkersORM
from models.workers import WorkersORM
from schemas.projects import ProjectQualityDTO, ProjectReportDTO, ProjectDTO
from schemas.workers import WorkerReportDTO, WorkerDTO


WorkerReportDTO.model_rebuild()
ProjectReportDTO.model_rebuild()


async def get_development_quality() -> list[ProjectQualityDTO]:
    session: AsyncSession
    async with (async_session_factory() as session):
        query = (
            select(ProjectsORM)
            .where(ProjectsORM.end_date != None)
            .order_by(ProjectsORM.start_date)
            .options(
                selectinload(ProjectsORM.plan_blocks)
                .selectinload(PlanBlocksORM.block_bugs)
            )
        )

        projects_with_blocks = (await session.execute(query)).scalars().all()
        projects_qualities: list[ProjectQualityDTO] = []

        for project in projects_with_blocks:
            start_date: datetime.datetime = project.start_date
            end_date: datetime.datetime = project.end_date
            project_duration: int = (end_date - start_date).days
            if project_duration == 0:
                project_duration = 1
            bug_cnt = 0
            for plan_block in project.plan_blocks:
                bug_cnt += len(plan_block.block_bugs)

            projects_qualities.append(ProjectQualityDTO(
                project_name=project.name,
                quality=bug_cnt/project_duration
            ))

        return projects_qualities


async def personal_list() -> list[WorkerReportDTO]:
    session: AsyncSession
    async with (async_session_factory() as session):
        query = (
            select(WorkersORM)
            .options(selectinload(WorkersORM.projects))
            .order_by(WorkersORM.fire_date.desc(), WorkersORM.username)
        )

        workers_orm = (await session.execute(query)).scalars().all()

        return [WorkerReportDTO.model_validate(worker, from_attributes=True) for worker in workers_orm]


async def projects_list() -> list[ProjectReportDTO]:
    session: AsyncSession
    async with async_session_factory() as session:
        query = (
            select(ProjectsORM)
            .options(selectinload(ProjectsORM.workers))
            .order_by(ProjectsORM.end_date.desc(), ProjectsORM.name)
        )

        projects_orm = (await session.execute(query)).scalars().all()

        return [ProjectReportDTO.model_validate(project, from_attributes=True) for project in projects_orm]
