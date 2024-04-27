// Stylesheets
import "../assets/ProjectsCard.css"

// Modules
import {useNavigate} from "react-router";
import axios from "axios";

// My components
import DeleteButton from "../../../components/DeleteButton.tsx";

// Interfaces
import {Project} from "../../../interfaces/project.ts";
import RestoreButton from "../../../components/RestoreButton.tsx";





interface Prop {
    project: Project
    onDelete: Function
    onRestore: Function
}


function ProjectsCard({project, onDelete, onRestore}: Prop) {
    let navigate = useNavigate()


    function projectNavigate() {
        navigate(`${project.id}`)
    }

    function deleteProject() {
        axios.delete(`http://localhost:8000/projects/${project.id}`).then(
            onDelete(project.id)
        )
    }

    function restoreProject() {
        axios.post(`http://localhost:8000/projects/${project.id}`).then(
            onRestore(project.id)
        )
    }

    return (
        <div className={`ProjectsCard${project.end_date == null ? "" : " Closed"}`}>
            <div className="Title">
                <p className="Text" onClick={projectNavigate}>{project.name}</p>
                {
                    project.end_date == null ?
                        <DeleteButton onClick={deleteProject}/>
                        :
                        <RestoreButton onClick={restoreProject}/>
                }
            </div>
            <div className="Description" onClick={projectNavigate}>
                <p className="Text">{project.description}</p>
            </div>
        </div>
    )
}

export default ProjectsCard
