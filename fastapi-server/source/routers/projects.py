from fastapi import APIRouter

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


@router.get("/{project_id}/workers", response_model=list[WorkerByProjectDTO])
async def get_workers_from_project(project_id: int):
    return await projects.get_workers_from_project(project_id)


@router.post("/")
async def add_project(project: ProjectAddDTO):
    await projects.add_project(project)
    return 200


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    await projects.close_project(project_id)
