from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from schemas.all import WorkerDTO, WorkerAddDTO, ProjectByWorkerDTO
from queries import workers
from schemas.plan_blocks import PlanBlockDTO
from schemas.workers import WorkerOnFireDTO
from send_email import send_email

router = APIRouter(
    prefix="/workers",
    tags=["workers"],
)


@router.get("/", response_model=list[WorkerDTO])
async def get_workers():
    return await workers.get_workers()


@router.get("/{worker_id}", response_model=WorkerDTO | None)
async def get_worker(worker_id: int, response: Response):
    worker = await workers.get_worker(worker_id)

    if worker is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return worker


@router.get("/search/{username_mask}", response_model=list[WorkerDTO])
async def search_workers(username_mask: str):
    return await workers.search_workers(username_mask)


@router.post("/", response_model=int | None)
async def add_worker(worker: WorkerAddDTO, response: Response):
    worker_id = await workers.add_worker(worker)
    if worker_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return worker_id


@router.delete("/{worker_id}", response_model=WorkerOnFireDTO | None)
async def delete_worker(worker_id: int, response: Response):
    worker = await workers.fire_worker(worker_id, "Решение начальства")
    if worker is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    else:
        await send_email(worker)
    return worker


@router.get("/{worker_id}/projects", response_model=list[ProjectByWorkerDTO])
async def get_projects_from_worker(worker_id: int):
    return await workers.get_projects_from_worker(worker_id)


@router.post("/transfer/{worker_id}/{new_project_id}")
async def transfer_worker(response: Response, worker_id: int, new_project_id: int):
    if not await workers.transfer_worker(worker_id, new_project_id, None):
        response.status_code = status.HTTP_400_BAD_REQUEST


@router.post("/transfer/{worker_id}/{new_project_id}/{old_project_id}")
async def transfer_worker(response: Response, worker_id: int, new_project_id: int, old_project_id):
    if not await workers.transfer_worker(worker_id, new_project_id, old_project_id):
        response.status_code = status.HTTP_400_BAD_REQUEST


@router.get("/{worker_id}/plan_blocks", response_model=list[PlanBlockDTO])
async def get_plan_blocks(worker_id: int):
    return await workers.get_plan_blocks(worker_id)
