import "../assets/ProjectsCard.css"
import {useNavigate} from "react-router";
import DeleteButton from "../../../components/DeleteButton.tsx";
import axios from "axios";
import {ProjectPage} from "../../project/ProjectPage.tsx";




interface Prop {
    project: Project
    onDelete: Function
}


function ProjectsCard({project, onDelete}: Prop) {
    let navigate = useNavigate()


    function projectNavigate() {
        navigate(`${project.id}`)
    }

    function deleteProject() {
        axios.delete(`http://localhost:8000/projects/${project.id}`).then(
            onDelete(project.id)
        )
    }

    return (
        <div className={`ProjectsCard${project.end_date == null ? "" : " Closed"}`}>
            <div className="Title">
                <p className="Text" onClick={projectNavigate}>{project.name}</p>
                <DeleteButton onClick={deleteProject}/>
            </div>
            <div className="Description" onClick={projectNavigate}>
                <p className="Text">{project.description}</p>
            </div>
        </div>
    )
}

export default ProjectsCard
