import datetime
import time

from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from engine import async_session_factory, async_engine
from models.test_models import TestModel1000, TestModel10000, TestModel100000


async def fill_tables():
    session: AsyncSession
    async with async_session_factory() as session:

        print("Adding a 1000-row table...")
        for i in range(1000):
            model = TestModel1000(
                name="some name",
                some_string="some string",
                date=datetime.datetime.now(),
                fake_unique=str(i)
            )
            session.add(model)

        print("Adding a 10000-row table...")
        for i in range(10000):
            model = TestModel10000(
                name="some name",
                some_string="some string",
                date=datetime.datetime.now(),
                fake_unique=str(i)
            )
            session.add(model)

        print("Adding a 10000-row table...")
        for i in range(100000):
            model = TestModel100000(
                name="some name",
                some_string="some string",
                date=datetime.datetime.now(),
                fake_unique=str(i)
            )
            session.add(model)

        print("Pushing all data to database...")
        await session.commit()


async def do_tests(exp_num: int, query1000, query10000, query100000, do_commit: bool = False):
    async with async_session_factory() as session:
        open_query = (
            select(TestModel1000)
            .where(TestModel1000.id == 1)
        )
        await session.execute(open_query)

        for i in range(3):
            delta_time = 0
            for j in range(exp_num):
                start_time = time.time_ns()
                await session.execute(query1000 if i == 0 else (query10000 if i == 1 else query100000))
                end_time = time.time_ns()
                delta_time += (end_time - start_time) / exp_num / 1000
            print(f"{1000 * 10 ** i} строк - {int(delta_time)}")

        if do_commit:
            await session.commit()


async def search_by_key(exp_num: int):
    query1000 = (
        select(TestModel1000)
        .where(TestModel1000.id == 900)
    )
    query10000 = (
        select(TestModel10000)
        .where(TestModel10000.id == 9000)
    )
    query100000 = (
        select(TestModel100000)
        .where(TestModel100000.id == 12345)
    )

    print("Поиск по ключевому полю")
    await do_tests(exp_num, query1000, query10000, query100000)


async def search_by_non_key(exp_num: int):
    query1000 = (
        select(TestModel1000)
        .where(TestModel1000.fake_unique == "900")
    )
    query10000 = (
        select(TestModel10000)
        .where(TestModel10000.fake_unique == "9000")
    )
    query100000 = (
        select(TestModel100000)
        .where(TestModel100000.fake_unique == "90000")
    )

    print("Поиск по НЕ ключевому полю")
    await do_tests(exp_num, query1000, query10000, query100000)


async def search_by_mask(exp_num: int):
    query1000 = (
        select(TestModel1000)
        .where(TestModel1000.some_string.icontains("i"))
    )
    query10000 = (
        select(TestModel10000)
        .where(TestModel10000.some_string.icontains("i"))
    )
    query100000 = (
        select(TestModel100000)
        .where(TestModel100000.some_string.icontains("i"))
    )

    print("Поиск по маске")
    await do_tests(exp_num, query1000, query10000, query100000)


async def add_one_row(exp_num: int):
    query1000 = (
        insert(TestModel1000)
        .values(
            name="some name",
            some_string="some string",
            date=datetime.datetime.now(),
            fake_unique="1"
        )
    )
    query10000 = (
        insert(TestModel10000)
        .values(
            name="some name",
            some_string="some string",
            date=datetime.datetime.now(),
            fake_unique="1"
        )
    )
    query100000 = (
        insert(TestModel100000)
        .values(
            name="some name",
            some_string="some string",
            date=datetime.datetime.now(),
            fake_unique="1"
        )
    )

    print("Добавление записи")
    await do_tests(exp_num, query1000, query10000, query100000)


async def add_many_rows(exp_num: int):
    rows: list[dict[str, str]] = list()

    for i in range(100):
        rows.append({
            "name": "some name",
            "some_string": "some string",
            "date": datetime.datetime.now(),
            "fake_unique": "1"
        })

    query1000 = (
        insert(TestModel1000)
        .values(rows)
    )
    query10000 = (
        insert(TestModel10000)
        .values(rows)
    )
    query100000 = (
        insert(TestModel100000)
        .values(rows)
    )

    print("Добавление группы записей")
    await do_tests(exp_num, query1000, query10000, query100000)


async def update_row_by_key(exp_num: int):
    query1000 = (
        update(TestModel1000)
        .where(TestModel1000.id == 900)
        .values(some_string="changed some string")
    )
    query10000 = (
        update(TestModel10000)
        .where(TestModel10000.id == 9000)
        .values(some_string="changed some string")
    )
    query100000 = (
        update(TestModel100000)
        .where(TestModel100000.id == 90000)
        .values(some_string="changed some string")
    )

    print("Изменение записи по ключевому полю")
    await do_tests(exp_num, query1000, query10000, query100000, False)


async def update_row_by_non_key(exp_num: int):
    query1000 = (
        update(TestModel1000)
        .where(TestModel1000.fake_unique == "900")
        .values(some_string="changed some string")
    )
    query10000 = (
        update(TestModel10000)
        .where(TestModel10000.fake_unique == "9000")
        .values(some_string="changed some string")
    )
    query100000 = (
        update(TestModel100000)
        .where(TestModel100000.fake_unique == "90000")
        .values(some_string="changed some string")
    )

    print("Изменение записи по НЕ ключевому полю")
    await do_tests(exp_num, query1000, query10000, query100000)


async def delete_row_by_key(exp_num: int):
    query1000 = (
        delete(TestModel1000)
        .where(TestModel1000.id == 900)
    )
    query10000 = (
        delete(TestModel10000)
        .where(TestModel10000.id == 9000)
    )
    query100000 = (
        delete(TestModel100000)
        .where(TestModel100000.id == 90000)
    )
    print("Удаление записи по ключевому полю")
    await do_tests(exp_num, query1000, query10000, query100000)


async def delete_row_by_non_key(exp_num: int):
    query1000 = (
        delete(TestModel1000)
        .where(TestModel1000.fake_unique == "900")
    )
    query10000 = (
        delete(TestModel10000)
        .where(TestModel10000.fake_unique == "9000")
    )
    query100000 = (
        delete(TestModel100000)
        .where(TestModel100000.fake_unique == "90000")
    )
    print("Удаление записи по НЕ ключевому полю")
    await do_tests(exp_num, query1000, query10000, query100000)


async def delete_rows(exp_num: int):
    to_delete = range(100, 200)

    query1000 = (
        delete(TestModel1000)
        .where(TestModel1000.id.in_(to_delete))
    )
    query10000 = (
        delete(TestModel10000)
        .where(TestModel10000.id.in_(to_delete))
    )
    query100000 = (
        delete(TestModel100000)
        .where(TestModel100000.id.in_(to_delete))
    )

    print("Удаление группы записей")
    await do_tests(exp_num, query1000, query10000, query100000)


async def delete_rows_by_non_key(exp_num: int):
    to_delete = range(100, 200)
    to_delete = list(map(lambda el: str(el), to_delete))

    query1000 = (
        delete(TestModel1000)
        .where(TestModel1000.fake_unique.in_(to_delete))
    )
    query10000 = (
        delete(TestModel10000)
        .where(TestModel10000.fake_unique.in_(to_delete))
    )
    query100000 = (
        delete(TestModel100000)
        .where(TestModel100000.fake_unique.in_(to_delete))
    )

    print("Удаление группы записей по неключевому полю")
    await do_tests(exp_num, query1000, query10000, query100000)


async def delete_200_rows(exp_num: int):
    to_delete = range(100, 200)

    query1000 = (
        delete(TestModel1000)
        .where(TestModel1000.id.in_(to_delete))
    )
    query10000 = (
        delete(TestModel10000)
        .where(TestModel10000.id.in_(to_delete))
    )
    query100000 = (
        delete(TestModel100000)
        .where(TestModel100000.id.in_(to_delete))
    )

    print("Удаление 200 записей по неключевому полю с коммитом")
    await do_tests(exp_num, query1000, query10000, query100000, True)


async def remain_200_rows(exp_num: int):
    to_delete1000 = range(200, 1000)
    to_delete10000 = range(200, 10000)
    to_delete100000 = range(200, 100000)

    query1000 = (
        delete(TestModel1000)
        .where(TestModel1000.id.in_(to_delete1000))
    )
    query10000 = (
        delete(TestModel10000)
        .where(TestModel10000.id.in_(to_delete10000))
    )
    query100000 = (
        delete(TestModel100000)
        .where(TestModel100000.id.in_(to_delete100000))
    )

    print("Оставление 200 записей по неключевому полю с коммитом")
    await do_tests(1, query1000, query10000, query100000, True)


async def vacuum_tables():
    print("Сжатие базы данных")
    conn: AsyncConnection
    async with async_engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        for i in range(3):
            start_time = time.time_ns()
            await conn.execute(text(f"VACUUM test_model_{1000 * 10 ** i}"))
            end_time = time.time_ns()
            delta_time = (end_time - start_time) / 1000
            print(f"{1000 * 10 ** i} строк - {int(delta_time)}")
