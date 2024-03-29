"""
This file contains workers-related pydantic schemas

Available schemas are
1. WorkerAddDTO
2. WorkerDTO
3. Workers
"""
from pydantic import BaseModel
import datetime

from database import MetaStr, DetailedInfoStr
from new_types import BugCategory, Level, SpecializationCode


class WorkerAddDTO(BaseModel):
    specialization_code: SpecializationCode
    passport_number: MetaStr
    username: MetaStr
    name: MetaStr
    surname: MetaStr
    patronymic: MetaStr | None
    email: MetaStr
    phone_number: MetaStr | None
    birthday: datetime.datetime | None
    level: Level


class WorkerDTO(WorkerAddDTO):
    id: int
    hire_date: datetime.datetime
    fire_date: datetime.datetime | None
    fire_reason: DetailedInfoStr | None
    overdue_count: int = 0


class WorkerWithRelDTO(WorkerDTO):
    projects: list["ProjectDTO"]
    plan_blocks: list["PlanBlockDTO"]


class WorkerByProjectDTO(WorkerDTO):
    project_hire_date: datetime.datetime
    project_fire_date: datetime.datetime | None

