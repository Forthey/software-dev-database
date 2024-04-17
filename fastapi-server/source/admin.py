from fastapi import FastAPI
from sqladmin import Admin, ModelView

from models import workers, projects, plan_blocks
from engine import async_engine

app = FastAPI()
admin = Admin(app, async_engine)


class WorkerAdmin(ModelView, model=workers.WorkersORM):
    name = "Worker"
    column_list = workers.WorkersORM.__table__.columns


class ProjectAdmin(ModelView, model=projects.ProjectsORM):
    name = "Project"
    column_list = projects.ProjectsORM.__table__.columns


class PlanBlockAdmin(ModelView, model=plan_blocks.PlanBlocksORM):
    name = "Plan Block"
    column_list = plan_blocks.PlanBlocksORM.__table__.columns


class PlanBlockTransferAdmin(ModelView, model=plan_blocks.PlanBlocksTransferORM):
    name = "Plan Block Transfer"
    column_list = plan_blocks.PlanBlocksTransferORM.__table__.columns


class BlockTestingAdmin(ModelView, model=plan_blocks.BlockTestingORM):
    name = "Block test"
    column_list = plan_blocks.BlockTestingORM.__table__.columns


class BlockBugAdmin(ModelView, model=plan_blocks.BlockBugsORM):
    name = "Block bug"
    column_list = plan_blocks.BlockBugsORM.__table__.columns


admin.add_view(WorkerAdmin)
admin.add_view(ProjectAdmin)
admin.add_view(PlanBlockAdmin)
admin.add_view(PlanBlockTransferAdmin)
admin.add_view(BlockTestingAdmin)
admin.add_view(BlockBugAdmin)
