from pydantic import BaseModel
import datetime

from database import MetaStr, DetailedInfoStr
from new_types import BugCategory, Level, SpecializationCode


class WorkersAddDTO(BaseModel):
    specialization_code: SpecializationCode
    passport_number: MetaStr
    username: MetaStr
    name: MetaStr
    surname: MetaStr
    patronymic: MetaStr | None
    email: MetaStr
    phone_number: MetaStr | None
    birthday: datetime.datetime | None


class WorkersDTO(WorkersAddDTO):
    id: int
    hire_date: datetime.datetime
    fire_date: datetime.datetime | None
    fire_reason: DetailedInfoStr | None


class WorkersRelDTO(WorkersDTO):
    projects: list["ProjectsDTO"]
    plan_blocks: list["PlanBlocksDTO"]


class WorkersByProjectDTO(WorkersDTO):
    project_hire_date: datetime.datetime
    project_fire_date: datetime.datetime | None

