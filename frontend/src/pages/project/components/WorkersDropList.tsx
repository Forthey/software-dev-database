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


interface Props {
    project_id: number
}

function WorkerSearchForm({project_id}: Props) {
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [workers, setWorkers] = useState<Worker[]>([])

    function setWorkersDataList(usernameMask: string) {
        if (usernameMask.length < 1) {
            return
        }

        setUsername(usernameMask)

        axios.get<Worker[]>(`http://localhost:8000/workers/search/${usernameMask}`)
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
                   onChange={event => setWorkersDataList(event.target.value)} list="WorkersDataList"></input>
            <datalist id="WorkersDataList">
                {
                    workers.filter(worker => worker.fire_date == null).map(worker =>
                        <option value={worker.username} key={worker.id}>{`${worker.surname} ${worker.name}`} </option>
                    )
                }
            </datalist>
            <TextButton onClick={addWorkerToProject} text="Добавить"/>
        </div>
    )
}

interface WorkerRowProps {
    worker: WorkerByProject
}


function WorkerRow({worker}: WorkerRowProps) {
    const navigate = useNavigate()

    function WorkerNavigate() {
        navigate(`/workers/${worker.id}`)
    }

    return (
        <div className="WorkersTableRow">
            <p className="Clickable" onClick={WorkerNavigate}>{worker.username}</p>
            <p className="Clickable" onClick={WorkerNavigate}>{worker.surname}</p>
            <p className="Clickable" onClick={WorkerNavigate}>{worker.name}</p>
            <p>{(new Date(worker.project_hire_date.toString())).toDateString()}</p>
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
                        <p>Дата принятия</p>
                    </div>
                    <div className="WorkersTableBody">
                        {
                            workers.filter(worker => worker.project_fire_date == null).map(worker =>
                                <WorkerRow worker={worker} key={worker.id} />
                            )
                        }
                    </div>
                </div>
            }
        </div>
    )
}

export default WorkersDropList