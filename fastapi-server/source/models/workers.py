from models.imports import *
from typing import TYPE_CHECKING


class Workers(Base):
    __tablename__ = "workers"

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

    projects: Mapped[list["Projects"]] = relationship(
        back_populates="workers",
        secondary="rel_projects_workers"
    )


class Developers(Base):
    __tablename__ = "developers"

    # В ForeignKey можно также передавать ORM класс напрямую, но
    # чаще всего классы разнесены по файлам и может возникнуть проблема с ключениями
    # Также в ForeignKey можно использовать поле ondelete="CASCADE", которая
    # при удалении работника удалит также и разработчика
    id: Mapped[IntPrimKey] = mapped_column(ForeignKey("Workers.id"), ondelete="CASCADE")
    overdue_count: Mapped[int] = 0
    level: Mapped[Level]

    developments: Mapped[list["Projects"]] = relationship()


class Testers(Base):
    __tablename__ = "Testers"

    id: Mapped[IntPrimKey] = mapped_column(ForeignKey("Workers.id"), ondelete="CASCADE")
    overdue_count: Mapped[int] = 0
    level: Mapped[Level]

    developments: Mapped[list["Projects"]] = relationship()
