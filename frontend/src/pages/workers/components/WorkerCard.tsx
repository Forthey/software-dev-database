// Stylesheets
import "../assets/WorkerCard.css"

// Modules
import {useNavigate} from "react-router";
import axios from "axios";
import DeleteButton from "../../../components/DeleteButton.tsx";

// Interfaces
import {Worker} from "../../../interfaces/worker.ts";


interface Prop {
    worker: Worker
    onDelete: Function
}

export const level = [
    "Intern",
    "Junior",
    "Middle",
    "Senior",
]

export const specialization = [
    "Программист",
    "Тестировщик"
]


function WorkerCard({worker, onDelete}: Prop) {
    const navigate = useNavigate()

    function goToWorker() {
        navigate(`${worker.id}`)
    }

    function deleteWorker() {
        axios.delete(`http://localhost:8000/workers/${worker.id}`).then(
            onDelete(worker.id)
        )
    }

    return (
        <div className={`WorkerCard${worker.fire_date == null ? "" : " Closed"}`}>
            <div className="Header">
                <p className="Username" onClick={goToWorker}>{worker.username}</p>
                <DeleteButton onClick={deleteWorker} />
            </div>
            <p className="FIO" onClick={goToWorker}>{worker.surname} {worker.name}</p>
            <p className="Email" onClick={goToWorker}>{worker.email}</p>
            <p className="LevelSpec" onClick={goToWorker}>{level[worker.level]} {specialization[worker.specialization_code]}</p>
            <div className="Overdue"><div className="Min">0</div><input type="range" min="0" max="7" defaultValue={worker.overdue_count}/><div className="Max">7</div></div>
        </div>
    )
}

export default WorkerCard