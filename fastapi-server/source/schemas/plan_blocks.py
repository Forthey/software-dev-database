from pydantic import BaseModel
import datetime

from database import MetaStr
from new_types import BugCategory, BlockStatus


class PlanBlockAddDTO(BaseModel):
    title: MetaStr
    project_id: int
    developer_id: int
    deadline: datetime.datetime


class PlanBlockDTO(PlanBlockAddDTO):
    id: int
    start_date: datetime.datetime
    end_date: datetime.datetime | None
    status: BlockStatus | None = None
    status_date: datetime.datetime | None = None


class PlanBlocksTransferDTO(BaseModel):
    id: int
    block_id: int
    tester_id: int
    new_status: BlockStatus
    date: datetime.datetime


class BlockTestingDTO(BaseModel):
    id: int
    block_id: int
    tester_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime | None
    deadline: datetime.datetime


class BlockBugAddDTO(BaseModel):
    title: MetaStr
    category: BugCategory


class BlockBugDTO(BlockBugAddDTO):
    id: int
    block_id: int
    tester_id: int
    detection_date: datetime.datetime
    deadline: datetime.datetime
    fix_date: datetime.datetime | None


class BlockWithTestAndBugs(PlanBlockDTO):
    block_testing: list[BlockTestingDTO]
    block_bugs: list[BlockBugDTO]
