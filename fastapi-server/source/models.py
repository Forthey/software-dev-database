# Для даты
import datetime
# Перечисляемый тип
import enum
from typing import Annotated
# Всё нужное для создания таблицы + метадата
from sqlalchemy import Table, Column, Integer, String, ForeignKey, text, MetaData, PrimaryKeyConstraint
# Для создания столбцов бд в ORM
from sqlalchemy.orm import Mapped, mapped_column
# Для своих типов
from sqlalchemy.types import UserDefinedType
# Базовый класс таблиц + типы
from database import Base, MetaStr, DetailedInfoStr


# Можно server_default = func.now() (func в sqlalchemy), но тогда будет записываться локальное время
IntPrimKey = Annotated[int, mapped_column(primary_key=True)]
CreateDate = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class SpecializationCode(enum.IntEnum):
    developer = 0
    tester = 1


class Level(enum.IntEnum):
    intern = 0
    junior = 1
    middle = 2
    senior = 3


class BugCategory(enum.IntEnum):
    minor = 0
    serious = 1
    showstopper = 2

class Workers(Base):
    __tablename__ = "Workers"

    id: Mapped[IntPrimKey]
    specialization_code: Mapped[SpecializationCode]
    passport_number: Mapped[str]
    username: Mapped[MetaStr] = mapped_column(unique=True)
    name: Mapped[MetaStr]
    surname: Mapped[MetaStr]
    patronymic: Mapped[MetaStr | None]
    email: Mapped[str]
    phone_number: Mapped[str | None]
    birthday: Mapped[datetime.datetime | None]
    hire_date: Mapped[CreateDate]
    fire_date: Mapped[datetime.datetime | None]
    fire_reason: Mapped[DetailedInfoStr | None]


class Developers(Base):
    __tablename__ = "Developers"

    # В ForeignKey можно также передавать ORM класс напрямую, но
    # чаще всего классы разнесены по файлам и может возникнуть проблема с ключениями
    # Также в ForeignKey можно использовать поле ondelete="CASCADE", которая
    # при удалении работника удалит также и разработчика
    id: Mapped[IntPrimKey] = mapped_column(ForeignKey("Workers.id"))
    overdue_count: Mapped[int] = 0
    level: Mapped[Level]


class Testers(Base):
    __tablename__ = "Testers"

    id: Mapped[IntPrimKey] = mapped_column(ForeignKey("Workers.id"))
    overdue_count: Mapped[int] = 0
    level: Mapped[Level]


class Projects(Base):
    __tablename__ = "Projects"

    id: Mapped[IntPrimKey]
    name: Mapped[MetaStr]
    description: Mapped[DetailedInfoStr]
    start_date: Mapped[CreateDate]
    end_date: Mapped[datetime.datetime | None]


class RefDevelopmentsWorkers(Base):
    __tablename__ = "RefCompanyWorkers"

    developments_id: Mapped[int] = mapped_column(ForeignKey("Projects.id"))
    workers_id: Mapped[int] = mapped_column(ForeignKey("Workers.id"))
    hire_date: Mapped[CreateDate]
    fire_date: Mapped[datetime.datetime | None]

    PrimaryKeyConstraint(developments_id, workers_id)


class PlanBlocks(Base):
    __tablename__ = "PlanBlocks"

    id: Mapped[IntPrimKey]
    development_id: Mapped[int] = mapped_column(ForeignKey("Projects.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("Developers.id"))
    start_date: Mapped[CreateDate]
    deadline: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime | None]


class PlanBlocksTransfer(Base):
    __tablename__ = "PlanBlocksTransfer"

    id: Mapped[IntPrimKey]
    block_id: Mapped[int] = mapped_column(ForeignKey("PlanBlocks.id"))
    tester_id: Mapped[int] = mapped_column(ForeignKey("Testers.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("Developers.id"))


# TODO: table
class BlockTesting(Base):
    __tablename__ = "BlocksTesting"

    id: Mapped[IntPrimKey]


# TODO: table
class BlockBugs(Base):
    __tablename__ = "BlockBugs"

    id: Mapped[IntPrimKey]
    block_id: Mapped[int] = mapped_column(ForeignKey("PlanBlocks.id"))
    tester_id: Mapped[int] = mapped_column(ForeignKey("Testers.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("Developers.id"))
    detection_date: Mapped[CreateDate]
    deadline: Mapped[datetime.datetime]
    fix_date: Mapped[datetime.datetime | None]
    category: Mapped[BugCategory]

