from fastapi import APIRouter

from schemas.plan_blocks import PlanBlockDTO, BlockBugDTO, BlockTestingDTO, BlockBugAddDTO, PlanBlockAddDTO
from queries import plan_blocks


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


@router.get("/{plan_block_id}", response_model=PlanBlockDTO)
async def get_plan_block(plan_block_id: int):
    return await plan_blocks.get_plan_block(plan_block_id)


@router.post("/")
async def add_plan_block(plan_block: PlanBlockAddDTO):
    await plan_blocks.add_plan_block(plan_block)


@router.delete("/{plan_block_id}")
async def delete_plan_block(plan_block_id: int):
    await plan_blocks.close_plan_block(plan_block_id)

#
# Block testing
#


@router.get("/{plan_block_id}/tests", response_model=list[BlockTestingDTO])
async def get_block_tests(plan_block_id: int):
    return await plan_blocks.get_block_tests(plan_block_id)


@router.post("/{plan_block_id}/tests/{tester_id}")
async def add_block_test(plan_block_id: int, tester_id: int):
    await plan_blocks.send_block_to_test(plan_block_id, tester_id)


@router.delete("/{plan_block_id}/tests/{test_id}")
async def close_block_test(plan_block_id: int, test_id: int):
    await plan_blocks.close_block_test(test_id)


#
# Block bugs
#


@router.get("/{plan_block_id}/bugs", response_model=list[BlockBugDTO])
async def get_block_bugs(plan_block_id: int):
    return await plan_blocks.get_block_bugs(plan_block_id)


@router.post("/{plan_block_id}/bugs")
async def add_block_bug(plan_block_id: int, block_bugs: list[BlockBugAddDTO]):
    await plan_blocks.add_block_bugs(block_bugs)


@router.delete("/{plan_block_id}/bugs/{block_bug_id}")
async def close_block_bug(plan_block_id: int, block_bug_id: int):
    await plan_blocks.close_block_bug(block_bug_id)
