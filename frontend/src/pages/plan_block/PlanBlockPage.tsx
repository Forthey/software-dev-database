// Stylesheets
import "./assets/PlanBlockPage.css"

// Modules
import {useParams} from "react-router";
import {useEffect, useState} from "react";
import axios from "axios";

// Interfaces
import {PlanBlock} from "../../interfaces/plan_block.ts";


function PlanBlockPage() {
    const params = useParams()
    const project_id = params.project_id
    const id = params.id
    const [planBlock, setPlanBlock] = useState<PlanBlock>()

    useEffect(() => {
        axios.get<PlanBlock>(`http://localhost:8000/projects/${project_id}/plan_blocks/${id}`)
            .then(response => setPlanBlock(response.data))
            .catch(() => alert("Такого проекта или блока не существует"))
    }, []);

    if (planBlock == undefined) {
        return (
            <></>
        )
    }

    return (
        <div className="PlanBlockPage">
            <p>{planBlock.title}</p>
        </div>
    )
}

export default PlanBlockPage