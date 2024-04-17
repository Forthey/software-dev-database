// Stylesheets
import "../assets/ProjectsDropList.css"

// Modules
import {useEffect, useState} from "react";
import axios from "axios";

// Interfaces
import {Project, ProjectByWorker} from "../../../interfaces/project.ts";
import TransferButton from "../../../components/TransferButton.tsx";
import {useNavigate} from "react-router";


interface Props {
    worker_id: number
}


interface ProjectRowProps {
    worker_id: number
    project: ProjectByWorker
}


function ProjectRow({worker_id, project}: ProjectRowProps) {
    const [projectName, setProjectName] = useState<string>("")
    const [projects, setProjects] = useState<Project[]>([])
    const navigate = useNavigate()


    function setProjectsDataList(nameMask: string) {
        if (nameMask.length < 1) {
            return
        }

        setProjectName(nameMask)

        axios.get<Project[]>(`http://localhost:8000/projects/search/${nameMask}`)
            .then(response => setProjects(response.data))
    }

    function Transfer() {
        const newProject = projects.find(project => project.name == projectName)

        if (newProject != undefined) {
            axios.post(`http://localhost:8000/workers/transfer/${worker_id}/${newProject.id}/${project.id}`)
                .then(() => navigate(0))
                .catch(() => alert("Такой трансфер провести нельзя"))
        }
    }

    return (
        <div className={`ProjectsTableRow${project.project_fire_date != null ? " Closed" : ""}`}>
            <p>{project.name}</p>
            <p>{project.description}</p>
            <p>{(new Date(project.project_hire_date)).toDateString()}</p>
            <div>
                <input type="text" placeholder="Имя проекта"
                       onChange={event => setProjectsDataList(event.target.value)} list="ProjectsDataList">
                </input>
                <datalist id="ProjectsDataList">
                    {
                        projects.filter(project => project.end_date == null).map(project =>
                            <option value={project.name} key={project.id}></option>
                        )
                    }
                </datalist>
                <TransferButton onClick={Transfer}/>
            </div>
        </div>
    )
}


function ProjectsDropList({worker_id}: Props) {
    const [projects, setProjects] = useState<ProjectByWorker[]>([])

    useEffect(() => {
        axios.get<ProjectByWorker[]>(`http://localhost:8000/workers/${worker_id}/projects`)
            .then(response => setProjects(response.data))
            .catch(() => alert(`Работника ${worker_id} не существует`))
    }, []);

    return (
        <div className="ProjectsDropList">
            <div className="DropListHeader">
                Проекты
            </div>
            <div className="ProjectsTable">
                <div className="ProjectsTableHead">
                    <p>Название</p>
                    <p>Описание</p>
                    <p>Дата принятия</p>
                    <p>Трансфер</p>
                </div>
                <div className="ProjectsTableBody">
                    {
                        projects.map(project =>
                            <ProjectRow project={project} worker_id={worker_id} key={project.id}/>
                        )
                    }
                </div>
            </div>
        </div>
    )
}

export default ProjectsDropList
