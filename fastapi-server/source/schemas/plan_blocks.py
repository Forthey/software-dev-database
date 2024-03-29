from pydantic import BaseModel
import datetime

from database import MetaStr
from new_types import BugCategory


class PlanBlockAddDTO(BaseModel):
    title: MetaStr
    project_id: int
    developer_id: int


class PlanBlockDTO(PlanBlockAddDTO):
    id: int
    start_date: datetime.datetime
    deadline: datetime.datetime
    end_date: datetime.datetime


class PlanBlocksTransferDTO(BaseModel):
    id: int
    block_id: int
    tester_id: int
    developer_id: int
    date: datetime.datetime


class BlockTestingDTO(BaseModel):
    id: int
    block_id: int
    tester_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime


class BlockBugsDTO(BaseModel):
    id: int
    title: MetaStr
    block_id: int
    tester_id: int
    developer_id: int
    detection_date: datetime.datetime
    deadline: datetime.datetime
    fix_date: datetime.datetime | None
    category: BugCategory
