// Stylesheets
import "../assets/WorkersDropList.css"

// Modules
import {useEffect, useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router";

// My components
import TextButton from "../../../components/TextButton.tsx";
import DropListHeader from "./DropListHeader.tsx";

// Interfaces
import {Worker, WorkerByProject} from "../../../interfaces/worker.ts";
import {levelToStr, specCodeToStr} from "../../../interfaces/enums.ts";
import DeleteButton from "../../../components/DeleteButton.tsx";


interface Props {
    project_id: number
}

function WorkerSearchForm({project_id}: Props) {
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [workers, setWorkers] = useState<Worker[]>([])

    function setWorkersDataList(usernameMask: string) {
        setUsername(usernameMask)

        axios.get<Worker[]>(`http://localhost:8000/workers/search/`, {params: {username_mask: usernameMask}})
            .then(response => {
                setWorkers(response.data)
            })
    }

    function addWorkerToProject() {
        const worker = workers.find(worker => worker.username == username)

        if (worker != undefined) {
            axios.post(`http://localhost:8000/workers/transfer/${worker.id}/${project_id}`)
                .then(() => navigate(0))
                .catch(() => alert("Превышено максимальное количество проектов для работника"))
        }
    }


    return (
        <div className="WorkersSearchForm">
            <input className="WorkerUsername" placeholder="Username пользователя"
                   onChange={event => setWorkersDataList(event.target.value)}
                   onFocus={event => setWorkersDataList(event.target.value)}
                   list="WorkersDataList"></input>
            <datalist id="WorkersDataList">
                {
                    workers.filter(worker => worker.fire_date == null).map(worker =>
                        <option value={worker.username} key={worker.id}>
                            {`${worker.surname} ${worker.name}\n${levelToStr[worker.level]} ${specCodeToStr[worker.specialization_code]}`}
                        </option>
                    )
                }
            </datalist>
            <TextButton onClick={addWorkerToProject} text="Добавить"/>
        </div>
    )
}

interface WorkerRowProps {
    project_id: number
    worker: WorkerByProject
}


function WorkerRow({project_id, worker}: WorkerRowProps) {
    const navigate = useNavigate()

    function WorkerNavigate() {
        navigate(`/workers/${worker.id}`)
    }

    function fireWorkerFromProject() {
        axios.delete(`http://localhost:8000/workers/${worker.id}/projects/${project_id}`)
            .then(() => navigate(0))
    }

    return (
        <div className={`WorkersTableRow${worker.project_fire_date != null ? " Closed" : ""}`}>
            <p className="Clickable" onClick={WorkerNavigate}>{worker.username}</p>
            <p className="Clickable" onClick={WorkerNavigate}>{worker.surname}</p>
            <p className="Clickable" onClick={WorkerNavigate}>{worker.name}</p>
            <p>{levelToStr[worker.level]} {specCodeToStr[worker.specialization_code]}</p>
            <div>
                <p>{(new Date(worker.project_hire_date.toString())).toDateString()}</p>
                <DeleteButton onClick={fireWorkerFromProject}/>
            </div>
        </div>
    )
}


function WorkersDropList({project_id}: Props) {
    const [workers, setWorkers] = useState<WorkerByProject[]>([])
    // const [active, setActive] = useState(false)
    const [searchActive, setSearchActive] = useState(false)

    useEffect(() => {
        axios.get<WorkerByProject[]>(`http://localhost:8000/projects/${project_id}/workers`)
            .then(response => setWorkers(response.data))
    }, []);

    function addSearchWorker() {
        setSearchActive(!searchActive)
    }

    return (
        <div className="WorkersDropList">
            <DropListHeader title="Персонал проекта" onClick={addSearchWorker} />
            {
                searchActive ? (
                    <WorkerSearchForm project_id={project_id} />
                ) : (
                    <></>
                )
            }
            {
                <div className="WorkersTable">
                    <div className="WorkersTableHead">
                        <p>Username</p>
                        <p>Фамилия</p>
                        <p>Имя</p>
                        <p>Специализация</p>
                        <p>Дата принятия</p>
                    </div>
                    <div className="WorkersTableBody">
                        {
                            workers.map(worker =>
                                <WorkerRow project_id={project_id} worker={worker} key={worker.id} />
                            )
                        }
                    </div>
                </div>
            }
        </div>
    )
}

export default WorkersDropList