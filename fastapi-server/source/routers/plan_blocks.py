from datetime import timedelta

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from schemas.plan_blocks import PlanBlockDTO, BlockBugDTO, BlockTestingDTO, BlockBugAddDTO, PlanBlockAddDTO, \
    BlockWithTestAndBugs
from queries import plan_blocks, workers
from send_email import send_email

router = APIRouter(
    prefix="/projects/{project_id}/plan_blocks",
    tags=["plan_blocks"]
)


#
# Plan blocks
#


@router.get("/", response_model=list[PlanBlockDTO])
async def get_plan_blocks(project_id: int):
    return await plan_blocks.get_plan_blocks(project_id)


@router.get("/{plan_block_id}", response_model=PlanBlockDTO | None)
async def get_plan_block(plan_block_id: int, response: Response):
    plan_block = await plan_blocks.get_plan_block(plan_block_id)
    if plan_block is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return plan_block


@router.post("/")
async def add_plan_block(plan_block: PlanBlockAddDTO, response: Response):
    plan_block_id = await plan_blocks.add_plan_block(plan_block)
    if plan_block_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return plan_block_id


@router.delete("/{plan_block_id}", response_model=BlockWithTestAndBugs | None)
async def delete_plan_block(plan_block_id: int, response: Response):
    block_with_rel = await plan_blocks.close_plan_block(plan_block_id)
    if block_with_rel is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

    if (block_with_rel.end_date - block_with_rel.start_date).total_seconds() * 0.9 > \
            (block_with_rel.deadline - block_with_rel.start_date).total_seconds():
        worker = await workers.add_overdue(block_with_rel.developer_id)
        if worker is not None:
            await send_email(worker)
    for block_test in block_with_rel.block_testing:
        if block_test.end_date > block_test.deadline:
            worker = await workers.add_overdue(block_test.tester_id)
            if worker is not None:
                await send_email(worker)
    for block_bug in block_with_rel.block_bugs:
        if block_bug.fix_date > block_bug.deadline:
            worker = await workers.add_overdue(block_with_rel.developer_id)
            if worker is not None:
                await send_email(worker)

    return block_with_rel

#
# Block testing
#


@router.get("/{plan_block_id}/tests", response_model=list[BlockTestingDTO])
async def get_block_tests(plan_block_id: int):
    return await plan_blocks.get_block_tests(plan_block_id)


@router.post("/{plan_block_id}/tests/{tester_id}", response_model=int | None)
async def add_block_test(project_id: int, plan_block_id: int, tester_id: int, response: Response):
    block_test_id = await plan_blocks.send_block_to_test(project_id, plan_block_id, tester_id)
    if block_test_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return block_test_id


@router.delete("/{plan_block_id}/tests/{test_id}", response_model=BlockTestingDTO | None)
async def close_block_test(plan_block_id: int, test_id: int, response: Response):
    block_test = await plan_blocks.close_block_test(test_id)
    if block_test is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None
    if block_test.end_date > block_test.deadline:
        worker = await workers.add_overdue(block_test.tester_id)
        if worker is not None:
            await send_email(worker)
    return block_test


#
# Block bugs
#


@router.get("/{plan_block_id}/bugs", response_model=list[BlockBugDTO])
async def get_block_bugs(plan_block_id: int):
    return await plan_blocks.get_block_bugs(plan_block_id)


@router.post("/{plan_block_id}/bugs", response_model=int | None)
async def add_block_bug(project_id: int, plan_block_id: int, block_bug: BlockBugAddDTO, response: Response):
    block_bug_id = await plan_blocks.add_block_bug(project_id, plan_block_id, block_bug)
    if block_bug_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return block_bug_id


@router.delete("/{plan_block_id}/bugs/{block_bug_id}", response_model=BlockBugDTO)
async def close_block_bug(plan_block_id: int, block_bug_id: int, response: Response):
    block_bug = await plan_blocks.close_block_bug(block_bug_id)
    if block_bug is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None
    if block_bug.fix_date > block_bug.deadline:
        worker = await workers.add_overdue(block_bug.developer_id)
        if worker is not None:
            await send_email(worker)
    return block_bug
