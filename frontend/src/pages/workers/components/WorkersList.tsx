// Stylesheets
import "../assets/WorkersList.css"

// Modules
import axios from "axios";
import {useEffect, useState} from "react";

// My components
import WorkerCard from "./WorkerCard.tsx";

// Interfaces
import {Worker} from "../../../interfaces/worker.ts";


function WorkersList() {
    let [workers, setWorkers] = useState<Worker[]>([])

    useEffect(() => {
        axios.get<Worker[]>("http://localhost:8000/workers").then(response =>
            setWorkers(response.data.sort((a: Worker, b: Worker) => {
                if (a.fire_date == null && b.fire_date != null) {
                    return -1;
                }
                if (b.fire_date == null && a.fire_date != null) {
                    return 1;
                }
                return 0;
            }))
        )
    }, [])

    function removeWorker(id: number) {
        setWorkers(workers.map(worker =>
            worker.id != id ? worker : {...worker, fire_date: new Date()}
        ))
    }

    function restoreWorker(id: number) {
        setWorkers(workers.map(worker => worker.id != id ? worker : {...worker, fire_date: null}))
    }

    return (
        <div className="WorkersList">
            {
                workers.map(worker => <WorkerCard key={worker.id} worker={worker} onDelete={removeWorker} onRestore={restoreWorker}/>)
            }
        </div>
    )
}

export default WorkersList