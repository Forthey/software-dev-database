from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import projects, workers, plan_blocks, reports

# # Без изменения loop policy на винде asyncio не работает с psycopg
# if platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="Software dev app",
    description="# Software development app that allows to do smth idk I just wrote it for fun",
    version="0.1.0",
    responses={
        404: {"description": "Not found"},
        228: {"description": "Already exists"}
    }
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(projects.router)
app.include_router(workers.router)
app.include_router(plan_blocks.router)
app.include_router(reports.router)
