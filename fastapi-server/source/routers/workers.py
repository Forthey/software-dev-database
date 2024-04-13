from http import HTTPStatus

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from new_types import ResultInfo
from schemas.all import WorkerDTO, WorkerAddDTO, ProjectByWorkerDTO
from queries import workers


router = APIRouter(
    prefix="/workers",
    tags=["workers"],
)


@router.get("/", response_model=list[WorkerDTO])
async def get_workers():
    return await workers.get_workers()


@router.get("/{worker_id}", response_model=WorkerDTO)
async def get_worker(worker_id: int, response: Response):
    worker = await workers.get_worker(worker_id)

    if worker is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return worker


@router.get("/search/{username_mask}", response_model=list[WorkerDTO])
async def search_workers(username_mask: str):
    return await workers.search_workers(username_mask)


@router.post("/")
async def add_worker(worker: WorkerAddDTO, response: Response):
    result: ResultInfo = await workers.add_worker(worker)
    if result is ResultInfo.failure:
        response.status_code = status.HTTP_400_BAD_REQUEST


@router.delete("/{worker_id}")
async def delete_worker(worker_id: int):
    await workers.fire_worker(worker_id)


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
