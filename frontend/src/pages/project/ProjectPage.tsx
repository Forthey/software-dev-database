// Stylesheets
import "./assets/Project.css"

// Modules
import {useParams} from "react-router";
import {useEffect, useState} from "react";
import axios from "axios";
import WorkersDropList from "./components/WorkersDropList.tsx";
import PlanBlocksDropList from "./components/PlanBlocksDropList.tsx";

// Interfaces
import {Project} from "../../interfaces/project.ts";


function ProjectPage() {
    const params = useParams()
    const [project, setProject] = useState<Project>()

    useEffect(() => {
        axios.get<Project>(`http://localhost:8000/projects/${params.id}`)
            .then(({data}) => {
                setProject(data)
            })
            .catch(() => alert("Проекта не существует"))
    },[])

    if (project != undefined) {
        return (
            <div className="ProjectPage">
                <div className="Title">
                    <p className="Name">{project.name}</p>
                </div>
                <div className="Body">
                    <p className="Description">{project.description}</p>
                </div>
                <WorkersDropList project_id={project.id}/>
                <PlanBlocksDropList project_id={project.id} />
            </div>
        )}
    return (<div></div>)
}

export default ProjectPage
