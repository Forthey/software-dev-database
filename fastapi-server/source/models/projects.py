from models.imports import *


class Projects(Base):
    __tablename__ = "Projects"

    id: Mapped[IntPrimKey]
    name: Mapped[MetaStr]
    description: Mapped[DetailedInfoStr]
    start_date: Mapped[CreateDate]
    end_date: Mapped[datetime.datetime | None]


class RefProjectsWorkers(Base):
    __tablename__ = "RefCompanyWorkers"

    project_id: Mapped[int] = mapped_column(ForeignKey("Projects.id"))
    workers_id: Mapped[int] = mapped_column(ForeignKey("Workers.id"))
    project_hire_date: Mapped[CreateDate]
    project_fire_date: Mapped[datetime.datetime | None]

    PrimaryKeyConstraint(project_id, workers_id)
