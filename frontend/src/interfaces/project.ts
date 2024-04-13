export interface ProjectAdd {
    name: string
    description: string
}


export interface Project extends ProjectAdd {
    id: number
    start_date: Date
    end_date: Date | null
}


export interface ProjectByWorker extends Project {
    project_hire_date: Date
    project_fire_date: Date | null
}
