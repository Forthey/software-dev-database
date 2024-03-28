# Для для начала работы асинхронной функции
import asyncio

from fastapi import FastAPI
# Для проверки системы
from sys import platform


from queries.orm import AsyncORM
from queries import projects, workers

from schemas.workers import WorkersAddDTO
from schemas.projects import ProjectAddDTO

# Без изменения loop policy на винде asyncio не работает с psycopg
if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
API_ROOT = "api"


@app.post("/tmp")
async def create_tables():
    await AsyncORM.create_tables()


@app.post("/projects/add")
async def add_project(project: ProjectAddDTO):
    await projects.add_project(project)


@app.post("/workers/add")
async def add_worker(worker: WorkersAddDTO):
    await workers.add_worker(worker)
