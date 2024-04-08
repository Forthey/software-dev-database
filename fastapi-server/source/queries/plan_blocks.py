from sqlalchemy import select, func, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

# joinedload подходит только к many-to-one и one-to-one загрузке
# (так как, если "правых" строк больше, при join левые будут дублироваться (а это первичный ключ, такое))
# selectin подходит для one-to-many и many-to-many, так как делает два запроса:
# сначала выбирает "левые" строки, а затем подгружает соответсвующие им "правые" строки
from sqlalchemy.orm import joinedload, selectinload

from engine import async_session_factory
from models.workers import WorkersORM
from models.projects import ProjectsORM, RelProjectsWorkersORM
from models.plan_blocks import PlanBlocksORM, BlockTestingORM, BlockBugsORM, PlanBlocksTransferORM

from schemas.all import PlanBlockAddDTO

from new_types import BugCategory, Level, SpecializationCode


async def get_plan_blocks(project_id: int) -> Sequence[PlanBlocksORM]:
    session: AsyncSession
    with async_session_factory() as session:
        # TODO: I'll leave it here for a while, mask %thing%
        # PlanBlocksORM.development_id.contains("thing")
        query = (
            select(PlanBlocksORM)
            .where(PlanBlocksORM.project_id == project_id)
            .group_by(PlanBlocksORM.id)
        )
        result = await session.execute(query)
        plan_blocks = result.scalars().all()
        await session.commit()
        return plan_blocks
