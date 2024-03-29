from models.imports import *


class PlanBlocks(Base):
    __tablename__ = "plan_blocks"

    id: Mapped[IntPrimKey]
    project_id: Mapped[int] = mapped_column(ForeignKey("Projects.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("Developers.id"))
    start_date: Mapped[CreateDate]
    deadline: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime | None]

    project: Mapped["Projects"] = relationship()
    block_transfers: Mapped[list["PlanBlocksTransfer"]] = relationship()
    blog_tests: Mapped[list["BlockTesting"]] = relationship()
    block_bugs: Mapped[list["BlockBugs"]] = relationship()


class PlanBlocksTransfer(Base):
    __tablename__ = "plan_blocks_transfer"

    id: Mapped[IntPrimKey]
    block_id: Mapped[int] = mapped_column(ForeignKey("PlanBlocks.id"))
    tester_id: Mapped[int] = mapped_column(ForeignKey("Testers.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("Developers.id"))

    block: Mapped["PlanBlocks"] = relationship()


class BlockTesting(Base):
    __tablename__ = "blocks_testing"

    id: Mapped[IntPrimKey]

    block: Mapped["PlanBlocks"] = relationship()


class BlockBugs(Base):
    __tablename__ = "blocks_bugs"

    id: Mapped[IntPrimKey]
    block_id: Mapped[int] = mapped_column(ForeignKey("PlanBlocks.id"))
    tester_id: Mapped[int] = mapped_column(ForeignKey("Testers.id"))
    developer_id: Mapped[int] = mapped_column(ForeignKey("Developers.id"))
    detection_date: Mapped[CreateDate]
    deadline: Mapped[datetime.datetime]
    fix_date: Mapped[datetime.datetime | None]
    category: Mapped[BugCategory]

    block: Mapped["PlanBlocks"] = relationship()
