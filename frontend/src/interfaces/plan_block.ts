import {BlockStatus, BugCategory} from "./enums.ts";

export interface PlanBlockAdd {
    title: string
    project_id: number
    developer_id: number
    deadline: Date
}


export interface PlanBlock extends PlanBlockAdd {
    id: number
    start_date: Date
    end_date: Date
    status: BlockStatus
    status_date: Date
}

export interface BlockBugAdd {
    title: string
    tester_id: number
    block_id: number
    category: BugCategory
}

export interface BlockBug extends BlockBugAdd {
    id: number
    detection_date: Date
    deadline: Date
    fix_date: Date | null
}