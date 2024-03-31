from fastapi import APIRouter

from schemas.all import WorkerDTO, WorkerAddDTO, ProjectByWorkerDTO
from queries import workers


router = APIRouter(
    prefix="/workers",
    tags=["workers"],
)


@router.get("/", response_model=list[WorkerDTO])
async def get_workers():
    return await workers.get_workers()


@router.post("/")
async def add_worker(worker: WorkerAddDTO):
    await workers.add_worker(worker)


@router.delete("/{worker_id}")
async def delete_worker(worker_id: int):
    await workers.fire_worker(worker_id)


@router.get("/{worker_id}", response_model=WorkerDTO)
async def get_worker(worker_id: int):
    worker = await workers.get_worker(worker_id)

    if worker is None:
        return 404
    return worker


@router.get("/{worker_id}/projects", response_model=list[ProjectByWorkerDTO])
async def get_projects_from_worker(worker_id: int):
    return await workers.get_projects_from_worker(worker_id)


@router.post("/transfer")
async def transfer_worker(worker_id: int, new_project_id: int, old_project_id: int | None = None):
    await workers.transfer_worker(worker_id, new_project_id, old_project_id)
