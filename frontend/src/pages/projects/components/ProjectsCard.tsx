import "../assets/ProjectsCard.css"
import {useNavigate} from "react-router";


function ProjectsCard() {
    let navigate = useNavigate()


    function projectNavigate() {
        navigate("123")
    }

    return (
        <div className="ProjectsCard" onClick={projectNavigate}>
            <div className="Title">
                <div className="Text">Название проекта</div>
            </div>
            <div className="Description">
                <div className="Text">Описание проекта</div>
            </div>
        </div>
    )
}

export default ProjectsCard
