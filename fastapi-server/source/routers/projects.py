from fastapi import APIRouter

from schemas.projects import ProjectAddDTO, ProjectDTO
from queries import projects

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/", response_model=list[ProjectDTO])
async def get_projects():
    return await projects.get_projects()

# TODO
# @router.get("/projects/{project_id}", response_model=)


@router.post("/")
async def add_project(project: ProjectAddDTO):
    await projects.add_project(project)
    return 200


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    # TODO
    ...
