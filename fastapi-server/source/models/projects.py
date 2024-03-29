from models.imports import *


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[IntPrimKey]
    name: Mapped[MetaStr]
    description: Mapped[DetailedInfoStr]
    start_date: Mapped[CreateDate]
    end_date: Mapped[datetime.datetime | None]

    workers: Mapped[list["Workers"]] = relationship(
        back_populates="projects",
        secondary="rel_projects_workers"
    )


class RelProjectsWorkers(Base):
    __tablename__ = "rel_projects_workers"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("Projects.id", ondelete="CASCADE"),
        primary_key=True
    )

    workers_id: Mapped[int] = mapped_column(
        ForeignKey("Workers.id", ondelete="CASCADE"),
        primary_key=True
    )
    project_hire_date: Mapped[CreateDate]
    project_fire_date: Mapped[datetime.datetime | None]

    PrimaryKeyConstraint(project_id, workers_id)
