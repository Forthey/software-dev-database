from models.dependencies import *


class ProjectsORM(Base):
    __tablename__ = "projects"

    id: Mapped[IntPrimKey]
    name: Mapped[MetaStr] = mapped_column(unique=True)
    description: Mapped[DetailedInfoStr]
    start_date: Mapped[CreateDate]
    end_date: Mapped[datetime.datetime | None]

    workers: Mapped[list["WorkersORM"]] = relationship(
        back_populates="projects",
        secondary="rel_projects_workers",
        order_by="WorkersORM.username"
    )
    plan_blocks: Mapped[list["PlanBlocksORM"]] = relationship(
        back_populates="project"
    )
    

class RelProjectsWorkersORM(Base):
    __tablename__ = "rel_projects_workers"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        primary_key=True
    )

    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id"),
        primary_key=True
    )
    project_hire_date: Mapped[CreateDate]
    project_fire_date: Mapped[datetime.datetime | None]
