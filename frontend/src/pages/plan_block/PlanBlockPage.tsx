// Stylesheets
import "./assets/PlanBlockPage.css"

// Modules
import {useParams} from "react-router";
import {useEffect, useState} from "react";
import axios from "axios";

// My components
import PlanBlockDev from "./components/PlanBlockDev.tsx";
import PlanBlockTest from "./components/PlanBlockTest.tsx";

// Interfaces and enums
import {PlanBlock} from "../../interfaces/plan_block.ts";
import {BlockStatus, blockStatusToStr} from "../../interfaces/enums.ts";
import {Worker} from "../../interfaces/worker.ts";
import PlanBlockBugs from "./components/PlanBlockBugs.tsx";


function PlanBlockPage() {
    const params = useParams()
    const project_id = params.project_id
    const id = params.id
    const [worker, setWorker] = useState<Worker>()
    const [planBlock, setPlanBlock] = useState<PlanBlock>()

    useEffect(() => {
        axios.get<PlanBlock>(`http://localhost:8000/projects/${project_id}/plan_blocks/${id}`)
            .then(response => {
                setPlanBlock(response.data)
                if (response.data != undefined) {
                    if (response.data.status == BlockStatus.on_testing) {
                        axios.get<Worker>(`http://localhost:8000/projects/${project_id}/plan_blocks/${response.data.id}/tester`)
                            .then(response => setWorker(response.data))
                    }
                    else {
                        axios.get<Worker>(`http://localhost:8000/workers/${response.data.developer_id}`)
                            .then(response => setWorker(response.data))
                    }
                }
            })
            .catch(() => alert("Такого блока не существует"))
    }, []);

    if (planBlock == undefined) {
        return (
            <></>
        )
    }

    return (
        <div className="PlanBlockPage">
            <p className="PlanBlockTitle">Блок плана: {planBlock.title}</p>
            <p className="BlockStatus">Статус: {blockStatusToStr[planBlock.status]}</p>
            <p className="BlockTransfer">Последняя передача: {(new Date(planBlock.status_date)).toDateString()}</p>
            <p className="BlockDev">Работник: {worker != undefined ? `${worker.username} - ${worker.surname} ${worker.name}` : ""}</p>
            {
                planBlock.status == BlockStatus.in_progress ?
                    (<>
                        <PlanBlockDev project_id={Number(project_id)} plan_block_id={planBlock.id}/>
                        <PlanBlockBugs project_id={Number(project_id)} block_id={planBlock.id}/>
                    </>) : <PlanBlockTest project_id={Number(project_id)} plan_block_id={planBlock.id} tester_id={worker?.id}/>
            }
        </div>
    )
}

export default PlanBlockPage