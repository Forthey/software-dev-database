from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from schemas.all import ProjectAddDTO, ProjectDTO, WorkerByProjectDTO
from queries import projects, reports
from schemas.projects import ProjectOnCloseDTO, ProjectQualityDTO

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/", response_model=list[ProjectDTO])
async def get_projects():
    return await projects.get_projects()


@router.get("/{project_id}", response_model=ProjectDTO | None)
async def get_project(project_id: int, response: Response):
    project = await projects.get_project(project_id)
    if project is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return project


@router.get("/search/", response_model=list[ProjectDTO])
async def search_projects(name_mask: str):
    return await projects.search_projects(name_mask)


@router.post("/", response_model=int | None)
async def add_project(project: ProjectAddDTO, response: Response):
    result = await projects.add_project(project)
    if result is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result


@router.post("/{project_id}", response_model=ProjectDTO | None)
async def restore_project(project_id: int, response: Response):
    project = await projects.restore_project(project_id)
    if project is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return project


@router.delete("/{project_id}", response_model=ProjectOnCloseDTO | None)
async def delete_project(project_id: int, response: Response):
    result = await projects.close_project(project_id)
    if result is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result


@router.get("/{project_id}/workers", response_model=list[WorkerByProjectDTO])
async def get_workers_from_project(project_id: int):
    return await projects.get_workers_from_project(project_id)
