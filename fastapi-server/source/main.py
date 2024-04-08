from fastapi import FastAPI

from routers import projects, workers

# # Без изменения loop policy на винде asyncio не работает с psycopg
# if platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="Software dev app",
    description="# Software development app that allows to do smth idk I just wrote it for fun",
    version="0.1.0",
    responses={404: {"description": "Not found"}}
)

app.include_router(projects.router)
app.include_router(workers.router)
