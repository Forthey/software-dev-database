from pydantic import BaseModel
import datetime

from database import MetaStr, DetailedInfoStr
from new_types import BugCategory, Level, SpecializationCode


class ProjectAddDTO(BaseModel):
    name: MetaStr
    description: DetailedInfoStr


class ProjectDTO(ProjectAddDTO):
    id: int
    start_date: datetime.datetime
    end_date: datetime.datetime | None
