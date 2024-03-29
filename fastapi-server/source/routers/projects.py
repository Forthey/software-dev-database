from fastapi import APIRouter

from schemas.projects import ProjectAddDTO, ProjectDTO, ProjectWithRelDTO
from schemas.workers import WorkerDTO
from queries import projects

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/")
async def get_projects():
    return await projects.get_active_projects()


@router.get("/projects/{project_id}")
async def get_project(project_id: int):
    return await projects.get_project(project_id)


@router.post("/")
async def add_project(project: ProjectAddDTO):
    await projects.add_project(project)
    return 200


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    await projects.close_project(project_id)
