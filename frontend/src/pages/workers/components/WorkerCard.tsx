// Stylesheets
import "../assets/WorkerCard.css"

// Modules
import {useNavigate} from "react-router";
import axios from "axios";
import DeleteButton from "../../../components/DeleteButton.tsx";

// Interfaces and enums
import {Worker} from "../../../interfaces/worker.ts";
import RestoreButton from "../../../components/RestoreButton.tsx";
import {levelToStr, specCodeToStr} from "../../../interfaces/enums.ts";


interface Props {
    worker: Worker
    onDelete: Function
    onRestore: Function
}


function WorkerCard({worker, onDelete, onRestore}: Props) {
    const navigate = useNavigate()

    function goToWorker() {
        navigate(`${worker.id}`)
    }

    function deleteWorker() {
        axios.delete(`http://localhost:8000/workers/${worker.id}`)
            .then(onDelete(worker.id))
    }

    function restoreWorker() {
        axios.post(`http://localhost:8000/workers/${worker.id}`)
            .then(onRestore(worker.id))
    }

    return (
        <div className={`WorkerCard${worker.fire_date == null ? "" : " Closed"}`}>
            <div className="Header">
                <p className="Username" onClick={goToWorker}>{worker.username}</p>
                {
                    worker.fire_date == null ?
                        <DeleteButton onClick={deleteWorker} />
                        :
                        <RestoreButton onClick={restoreWorker}/>
                }
            </div>
            <p className="FIO" onClick={goToWorker}>{worker.surname} {worker.name}</p>
            <p className="Email" onClick={goToWorker}>{worker.email}</p>
            <p className="LevelSpec" onClick={goToWorker}>{levelToStr[worker.level]} {specCodeToStr[worker.specialization_code]}</p>
            <div className="Overdue">
                <div className="Min">0</div>
                <input type="range" min="0" max="7" defaultValue={worker.overdue_count}/>
                <div className="Max">7 ({worker.overdue_count})</div>
            </div>
        </div>
    )
}

export default WorkerCard