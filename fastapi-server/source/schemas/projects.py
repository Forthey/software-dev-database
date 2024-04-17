"""
This file contains project-related pydantic schemas

Available schemas are
1. ProjectAddDTO
2. ProjectDTO
3. ProjectWithRelDTO
"""


from pydantic import BaseModel
import datetime

from database import MetaStr, DetailedInfoStr


class ProjectAddDTO(BaseModel):
    name: MetaStr
    description: DetailedInfoStr


class ProjectDTO(ProjectAddDTO):
    id: int
    start_date: datetime.datetime
    end_date: datetime.datetime | None


class ProjectByWorkerDTO(ProjectDTO):
    project_hire_date: datetime.datetime
    project_fire_date: datetime.datetime | None


class ProjectOnCloseDTO(BaseModel):
    project_id: int
    workers_id: list[int]
    plan_blocks_id: list[int]


class ProjectQualityDTO(BaseModel):
    project_name: str
    quality: float


class ProjectReportDTO(ProjectDTO):
    workers: list["WorkerDTO"]
