// Stylesheets
import "../assets/ProjectsList.css"

// Modules
import {useEffect, useState} from "react";
import axios from "axios";

// My components
import ProjectsCard from "./ProjectsCard.tsx";

// Interfaces
import {Project} from "../../../interfaces/project.ts";


function ProjectsList() {
    const [projects, setProjects] = useState<Project[]>([])

    useEffect(() => {
        axios.get<Project[]>("http://localhost:8000/projects").then(
            (response) => {
                setProjects(response.data.sort((a: Project, b: Project) => {
                    if (a.end_date == null && b.end_date != null) {
                        return -1;
                    }
                    if (b.end_date == null && a.end_date != null) {
                        return 1;
                    }
                    return 0;


                }))
            }
        )
    }, [])

    function deleteProject(id: number) {
        setProjects(projects.map(project =>
                project.id != id ? project : {...project, end_date: new Date()}
        ))
    }

    function restoreProject(id: number) {
        setProjects(projects.map(project =>
            project.id != id ? project : {...project, end_date: null}
        ))
    }

    return (
        <div className="ProjectsList">
            {
                projects.map(project => <ProjectsCard project={project} key={project.id} onDelete={deleteProject} onRestore={restoreProject}/>)
            }
        </div>
    )
}

export default ProjectsList
