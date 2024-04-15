"""
This file contains workers-related pydantic schemas

Available schemas are
1. WorkerAddDTO
2. WorkerDTO
3. WorkerByProjectDTO
"""
from pydantic import BaseModel
import datetime

from database import MetaStr, DetailedInfoStr
from new_types import BugCategory, Level, SpecializationCode


class WorkerAddDTO(BaseModel):
    specialization_code: SpecializationCode
    username: MetaStr
    name: MetaStr
    surname: MetaStr
    email: MetaStr
    level: Level


class WorkerDTO(WorkerAddDTO):
    id: int
    hire_date: datetime.datetime
    fire_date: datetime.datetime | None
    fire_reason: DetailedInfoStr | None
    overdue_count: int = 0


class WorkerByProjectDTO(WorkerDTO):
    project_hire_date: datetime.datetime
    project_fire_date: datetime.datetime | None


class WorkerOnFireDTO(WorkerDTO):
    projects_id: list[int]
    plan_blocks_id: list[int]
    block_testings_id: list[int]
    block_bugs_id: list[int]
