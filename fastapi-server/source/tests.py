import asyncio

import queries.test_queries
from queries import test_queries


EXP_CNT = 1000


commands = [
    test_queries.fill_tables,
    test_queries.search_by_key,
    test_queries.search_by_non_key,
    test_queries.search_by_mask,
    test_queries.add_one_row,
    test_queries.add_many_rows,
    test_queries.update_row_by_key,
    test_queries.update_row_by_non_key,
    test_queries.delete_row_by_key,
    test_queries.delete_row_by_non_key,
    test_queries.delete_rows,
    test_queries.delete_rows_by_non_key,
    test_queries.delete_200_rows,
    test_queries.remain_200_rows,
    test_queries.vacuum_tables
]


async def start():
    print("0 - для заполнения таблиц, 14 - сжаите, 1-13 - для тестов, -1 - выход")
    a = 0
    while a != -1:
        try:
            a = int(input())
        except ValueError:
            print("Неверный ввод")

        if a == 0:
            await test_queries.fill_tables()
        elif a == 14:
            await test_queries.vacuum_tables()

        if 1 <= a <= 13:
            await commands[a](EXP_CNT)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(start())
