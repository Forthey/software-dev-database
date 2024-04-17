// Stylesheets
import "../assets/PlanBlockBugs.css"

// Modules
import axios from "axios";
import {useEffect, useState} from "react";

// Interfaces ans enums
import {BlockBug} from "../../../interfaces/plan_block.ts";
import {bugCategoryToStr} from "../../../interfaces/enums.ts";
import DeleteButton from "../../../components/DeleteButton.tsx";
import {useNavigate} from "react-router";


interface Props {
    project_id: number
    block_id: number
}

interface BlockBugRow {
    bug: BlockBug
    project_id: number
}

function BlockBugRow({bug, project_id}: BlockBugRow) {
    const navigate = useNavigate()

    function deleteBug() {
        axios.delete(`http://localhost:8000/projects/${project_id}/plan_blocks/${bug.block_id}/bugs/${bug.id}`)
            .then(() => navigate(0))
            .catch(() => alert("Что-то пошло не так"))
    }

    return (
        <div className="BlockBugRow">
            <p className="BugTitle">{bug.title}</p>
            <p className="BugCategory">{bugCategoryToStr[bug.category]}</p>
            <p className="BugDeadline"><p>{(new Date(bug.deadline)).toDateString()}</p> <DeleteButton onClick={deleteBug}/></p>
        </div>
    )
}

function PlanBlockBugs({project_id, block_id}: Props) {
    const [bugs, setBugs] = useState<BlockBug[]>([])

    useEffect(() => {
        axios.get<BlockBug[]>(`http://localhost:8000/projects/${project_id}/plan_blocks/${block_id}/bugs`)
            .then(response => setBugs(response.data))
    }, []);

    return (
        <div className="PlanBlockBugs">
            <p className="PlanBlockBugsHead">Баги</p>
            <div className="PlanBlockBugsTitle">
                <p>Что не так</p>
                <p>Категория</p>
                <p>Дедлайн</p>
            </div>
            <div className="PlanBlockBugsBody">
            {
                bugs.filter(bug => bug.fix_date == null)
                    .map(bug => <BlockBugRow key={bug.id} project_id={project_id} bug={bug}/>)
            }
            </div>
        </div>
    )
}

export default PlanBlockBugs