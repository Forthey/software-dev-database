import "../assets/WorkersList.css"
import axios from "axios";
import {useEffect, useState} from "react";
import WorkerCard from "./WorkerCard.tsx";
import {Worker} from "./WorkerCard.tsx";


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

    return (
        <div className="WorkersList">
            {
                workers.map(worker => <WorkerCard key={worker.id} worker={worker} onDelete={removeWorker}/>)
            }
        </div>
    )
}

export default WorkersList