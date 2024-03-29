from models.imports import *


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[IntPrimKey]
    name: Mapped[MetaStr]
    description: Mapped[DetailedInfoStr]
    start_date: Mapped[CreateDate]
    end_date: Mapped[datetime.datetime | None]

    developers: Mapped[list["Developers"]] = relationship(
        back_populates="projects",
        secondary="rel_projects_workers"
    )
    testers: Mapped[list["Testers"]] = relationship(
        back_populates="projects",
        secondary="rel_projects_workers"
    )
    plan_blocks: Mapped[list["PlanBlocks"]] = relationship()


class RelProjectsWorkers(Base):
    __tablename__ = "rel_projects_workers"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("Projects.id"),
        primary_key=True
    )

    workers_id: Mapped[int] = mapped_column(
        ForeignKey("Workers.id"),
        primary_key=True
    )
    project_hire_date: Mapped[CreateDate]
    project_fire_date: Mapped[datetime.datetime | None]
