from models.dependencies import *


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
    overdue_count: Mapped[int] = 0
    level: Mapped[Level]

    projects: Mapped[list["Projects"]] = relationship(
        back_populates="workers",
        secondary="rel_projects_workers"
    )
