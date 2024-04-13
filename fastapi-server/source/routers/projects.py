from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from new_types import ResultInfo
from schemas.all import ProjectAddDTO, ProjectDTO, WorkerByProjectDTO
from queries import projects

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/", response_model=list[ProjectDTO])
async def get_projects():
    return await projects.get_projects()


@router.get("/{project_id}", response_model=ProjectDTO)
async def get_project(project_id: int):
    return await projects.get_project(project_id)


@router.get("/search/{name_mask}", response_model=list[ProjectDTO])
async def search_projects(name_mask: str):
    return await projects.search_projects(name_mask)


@router.post("/")
async def add_project(project: ProjectAddDTO, response: Response):
    result: ResultInfo = await projects.add_project(project)
    if result is ResultInfo.failure:
        response.status_code = status.HTTP_400_BAD_REQUEST


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    await projects.close_project(project_id)


@router.get("/{project_id}/workers", response_model=list[WorkerByProjectDTO])
async def get_workers_from_project(project_id: int):
    return await projects.get_workers_from_project(project_id)
