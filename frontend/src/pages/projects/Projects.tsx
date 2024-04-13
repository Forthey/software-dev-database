import "./assets/Projects.css"
import "./components/ProjectsList.tsx"
import ProjectsList from "./components/ProjectsList.tsx";
import AddButton from "../../components/AddButton.tsx";
import {useNavigate} from "react-router";


function Projects() {
    let navigate = useNavigate()

    function addProjectNavigate() {
        navigate("add")
    }

    return (
        <div className="ProjectsPage">
            <AddButton onClick={addProjectNavigate} />
            <ProjectsList />
        </div>
    )
}

export default Projects