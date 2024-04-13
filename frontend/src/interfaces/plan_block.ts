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
}
