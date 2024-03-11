# Для для начала работы асинхронной функции
import asyncio
# Для проверки системы
from sys import platform

# from queries.orm import AsyncORM

# Без изменения loop policy на винде asyncio не работает с psycopg
if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# asyncio.run(AsyncORM.create_tables())
