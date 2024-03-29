from fastapi import APIRouter

from schemas.workers import WorkersDTO, WorkersAddDTO
from queries import workers


router = APIRouter(
    prefix="/workers",
    tags=["workers"],
)


@router.post("/")
async def add_worker(worker: WorkersAddDTO):
    await workers.add_worker(worker)


@router.get("/{worker_id}", response_model=WorkersDTO)
async def get_worker(worker_id: int):
    worker = await workers.get_worker(worker_id)

    if worker is None:
        return 404
    return worker
