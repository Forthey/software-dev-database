from models.imports import *


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
