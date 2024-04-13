// Stylesheets
import "./assets/Worker.css"

// Modules
import {useParams} from "react-router";
import {useEffect, useState} from "react";
import axios from "axios";

// My components

// Interfaces
import {Worker} from "../../interfaces/worker.ts";
import ProjectsDropList from "./components/ProjectsDropList.tsx";



function WorkerPage() {
    const params = useParams()
    const [worker, setWorker] = useState<Worker>()

    useEffect(() => {
        axios.get<Worker>(`http://localhost:8000/workers/${params.id}`)
            .then(response =>
                setWorker(response.data)
            )
    }, []);

    if (worker != undefined) {
        return (
            <div className="WorkerPage">
                <div className="Title">
                    <p>{worker.username}</p>
                </div>
                <div className="Body">
                    <p>{worker.surname} {worker.name}</p>
                    <p>{(new Date(worker.hire_date)).toDateString()} - {worker.fire_date ? (new Date(worker.fire_date)).toDateString() : "..."}</p>
                </div>
                <ProjectsDropList worker_id={worker.id} />
            </div>
        )
    }
    return (<></>)
}

export default WorkerPage
