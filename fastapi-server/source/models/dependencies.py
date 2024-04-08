# Всё нужное для создания таблицы + метадата
from sqlalchemy import ForeignKey, text
# Для создания столбцов бд в ORM
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Базовый класс таблиц + типы
from database import Base, MetaStr, DetailedInfoStr

# Для даты
import datetime

# Для добавления метадаты к столбцам: макс длина строки и т.п.
from typing import Annotated

# Новые типы
from new_types import SpecializationCode, Level, BugCategory

# Можно server_default = func.now() (func в sqlalchemy), но тогда будет записываться локальное время
IntPrimKey = Annotated[int, mapped_column(primary_key=True)]
CreateDate = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
