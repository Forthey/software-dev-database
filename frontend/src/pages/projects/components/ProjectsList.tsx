import "../assets/ProjectsList.css"
import ProjectsCard from "./ProjectsCard.tsx";
import AddButton from "./AddButton.tsx";

function ProjectsList() {
    return (
        <div className="ProjectsList">
            <AddButton />
            <ProjectsCard />
            <ProjectsCard />
            <ProjectsCard />
            <ProjectsCard />
            <ProjectsCard />
            <ProjectsCard />
            <ProjectsCard />
            <ProjectsCard />
        </div>
    )
}

export default ProjectsList
