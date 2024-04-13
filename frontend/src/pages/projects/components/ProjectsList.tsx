import "../assets/ProjectsList.css"
import ProjectsCard from "./ProjectsCard.tsx";
import {ProjectPage} from "../../project/ProjectPage.tsx";
import {useEffect, useState} from "react";
import axios from "axios";



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

    return (
        <div className="ProjectsList">
            {
                projects.map(project => <ProjectsCard project={project} key={project.id} onDelete={deleteProject}/>)
            }
        </div>
    )
}

export default ProjectsList
