# Для для начала работы асинхронной функции
import asyncio
from fastapi import FastAPI
# Для проверки системы
from sys import platform

from queries.orm import AsyncORM

# Без изменения loop policy на винде asyncio не работает с psycopg
if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()


@app.post("/projects")
async def get_company_projects():
    ...


@app.post("/projects/start/")
async def start_project():
    ...


@app.post("/worker/hire")
async def hire_worker():
    ...


@app.post("/worker/transfer")
async def transfer_worker():
    ...


@app.post("/project/close")
async def close_project(project_id: int):
    ...


@app.post("/project/{project_id}")
async def get_project_info(project_id: int):
    ...


@app.post("/reports/projects/active")
async def get_report_of_active_projects():
    ...


@app.post("/reports/workers")
async def get_report_of_workers():
    ...


@app.post("/reports/quality")
async def get_report_of_quality():
    ...


# asyncio.run(AsyncORM.create_tables())
