import "./components/ProjectsList.tsx"
import ProjectsList from "./components/ProjectsList.tsx";
import HomeButton from "../../components/HomeButton.tsx";


function Projects() {
    return (
        <div>
            <HomeButton />
            <ProjectsList />
        </div>
    )
}

export default Projects