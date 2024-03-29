from models.dependencies import *


class PlanBlocks(Base):
    __tablename__ = "plan_blocks"

    id: Mapped[IntPrimKey]
    title: Mapped[MetaStr]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    start_date: Mapped[CreateDate]
    deadline: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime | None]

    project: Mapped["Projects"] = relationship(
        back_populates="plan_blocks",
        cascade="all,delete"
    )
    block_transfers: Mapped[list["PlanBlocksTransfer"]] = relationship(
        back_populates="block"
    )
    block_testing: Mapped[list["BlockTesting"]] = relationship(
        back_populates="block"
    )
    block_bugs: Mapped[list["BlockBugs"]] = relationship(
        back_populates="block"
    )


class PlanBlocksTransfer(Base):
    __tablename__ = "plan_blocks_transfer"

    id: Mapped[IntPrimKey]
    block_id: Mapped[int] = mapped_column(ForeignKey("plan_blocks.id"))
    tester_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    date: Mapped[CreateDate]

    block: Mapped["PlanBlocks"] = relationship(
        back_populates="block_transfers"
    )


class BlockTesting(Base):
    __tablename__ = "blocks_testing"

    id: Mapped[IntPrimKey]
    block_id: Mapped[int] = mapped_column(ForeignKey("plan_blocks.id"))
    tester_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    start_date: Mapped[CreateDate]
    end_date: Mapped[datetime.datetime]

    block: Mapped["PlanBlocks"] = relationship(
        back_populates="block_testing"
    )


class BlockBugs(Base):
    __tablename__ = "blocks_bugs"

    id: Mapped[IntPrimKey]
    title: Mapped[MetaStr]
    block_id: Mapped[int] = mapped_column(ForeignKey("plan_blocks.id"))
    tester_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    detection_date: Mapped[CreateDate]
    deadline: Mapped[datetime.datetime]
    fix_date: Mapped[datetime.datetime | None]
    category: Mapped[BugCategory]

    block: Mapped["PlanBlocks"] = relationship(
        back_populates="block_bugs",
        cascade="all,delete"
    )
