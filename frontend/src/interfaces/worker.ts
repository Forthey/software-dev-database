
export interface WorkerAdd {
    specialization_code: number
    username: string
    name: string
    surname: string
    email: string
    level: number
}

export interface Worker extends WorkerAdd {
    id: number
    hire_date: Date
    fire_date: Date | null
    fire_reason: string | null
    overdue_count: number
}

export interface WorkerByProject extends Worker {
    project_hire_date: Date
    project_fire_date: Date | null
}