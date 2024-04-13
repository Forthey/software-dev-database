from models.dependencies import *


class WorkersORM(Base):
    __tablename__ = "workers"

    id: Mapped[IntPrimKey]
    specialization_code: Mapped[SpecializationCode]
    username: Mapped[MetaStr] = mapped_column(unique=True)
    name: Mapped[MetaStr]
    surname: Mapped[MetaStr]
    email: Mapped[str]
    hire_date: Mapped[CreateDate]
    fire_date: Mapped[datetime.datetime | None]
    fire_reason: Mapped[DetailedInfoStr | None]
    overdue_count: Mapped[int] = 0
    level: Mapped[Level]

    projects: Mapped[list["ProjectsORM"]] = relationship(
        back_populates="workers",
        secondary="rel_projects_workers"
    )
