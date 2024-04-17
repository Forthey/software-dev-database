from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from new_types import level_str, spec_code_str
from queries import reports
from schemas.projects import ProjectQualityDTO, ProjectReportDTO
from schemas.workers import WorkerReportDTO

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)


@router.get("/quality", response_model=list[ProjectQualityDTO])
async def get_projects_report():
    return await reports.get_development_quality()


def personal_list_to_md(personal_list: list[WorkerReportDTO]) -> str:
    result_md = "# Список персонала\n"

    for worker in personal_list:
        result_md += (
            f"## {worker.username}: {worker.surname} {worker.name}\n"
            f"#### {level_str[worker.level]} {spec_code_str[worker.specialization_code]}\n"
            f"#### {worker.hire_date.date()} - {worker.fire_date.date() if worker.fire_date else "..."}\n"
            f"### Проекты\n"
        )

        if len(worker.projects) == 0:
            result_md += "- Не учавствовал в проектах\n"
        for project in worker.projects:
            result_md += (
                f"- {project.name}\n"
                f"  - {project.description}\n"
                f"  - {project.start_date.date()} - {project.end_date.date() if project.end_date else "..."}\n"
            )
    return result_md


@router.get("/workers", response_class=PlainTextResponse)
async def get_workers_list():
    return personal_list_to_md(await reports.personal_list())


def project_list_to_md(project_list: list[ProjectReportDTO]) -> str:
    result_md = "# Список проектов\n"

    for project in project_list:
        result_md += (
            f"## {project.name}\n"
            f"#### {project.description}\n"
            f"#### {project.start_date.date()} - {project.end_date.date() if project.end_date else "..."}\n"
            f"### Персонал\n"
        )

        if len(project.workers) == 0:
            result_md += "- Персонал отсутствует\n"
        for worker in project.workers:
            result_md += (
                f"- {worker.username}: {worker.surname} {worker.name}\n"
                f"  - {level_str[worker.level]} {spec_code_str[worker.specialization_code]}\n"
                f"  - {worker.hire_date.date()} - {worker.fire_date.date() if worker.fire_date else "..."}\n"
            )
    return result_md


@router.get("/projects", response_class=PlainTextResponse)
async def get_projects_list():
    return project_list_to_md(await reports.projects_list())
