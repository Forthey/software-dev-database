// Stylesheets
import "../assets/PlanBlocksDropList.css"

// Modules
import {useEffect, useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router";

// My components
import DropListHeader from "./DropListHeader.tsx";
import TextButton from "../../../components/TextButton.tsx";

// Interfaces
import {Worker} from "../../../interfaces/worker.ts";
import {PlanBlockAdd, PlanBlock} from "../../../interfaces/plan_block.ts"


interface Props {
    projectId: number
}


interface PlanBlockProps extends Props {
    planBlock: PlanBlock
}


function PlanBlockForm({projectId}: Props) {
    const [newPlanBlock, setNewPlanBlock] = useState<PlanBlockAdd>({
        title: "",
        project_id: projectId,
        developer_id: 0,
        deadline: new Date(Date.now() + 10 * 24 * 60 * 60 * 1000 )
    })
    const [workerUsername, setWorkerUsername] = useState<string>("")
    const [workers, setWorkers] = useState<Worker[]>([])
    const navigate = useNavigate()


    function setPlanBlockTitle(newTitle: string) {
        setNewPlanBlock({...newPlanBlock, title: newTitle})
    }

    function setWorkersDataList(usernameMask: string) {
        if (usernameMask.length < 1) {
            return
        }

        setWorkerUsername(usernameMask)

        axios.get<Worker[]>(`http://localhost:8000/workers/search/${usernameMask}`)
            .then(response => {
                setWorkers(response.data)
            }
        )
    }

    function setDeadline(deadlineStr: string) {
        setNewPlanBlock({...newPlanBlock, deadline: new Date(deadlineStr)})
    }

    function isInteger(value: string) {
        return /^\d+$/.test(value);
    }

    function addPlanBlock() {
        if (!isInteger(workerUsername)) {
            alert("В поле username в итоге должен быть выбранный id пользователя")
            return
        }

        newPlanBlock.developer_id = Number(workerUsername)

        axios.post<PlanBlockAdd>(`http://localhost:8000/projects/${projectId}/plan_blocks`, newPlanBlock)
            .then(() => navigate(0))
            .catch(() => alert("Нельзя добавить блок плана. Скорее всего, разработчик не находится в проекте"))
    }

    return (
        <div className="PlanBlockForm">
            <input className="PlanBlockTitle" placeholder="Имя блока"
                   onChange={event => setPlanBlockTitle(event.target.value)}></input>
            <input className="PlanBlockUserName" placeholder="Username пользователя"
                   onChange={event => setWorkersDataList(event.target.value)} list="WorkersDataList"></input>
            <datalist id="WorkersDataList">
                {
                    workers.filter(worker => worker.fire_date == null).map(worker =>
                        <option value={worker.id} key={worker.id}>{`${worker.username}`} </option>
                    )
                }
            </datalist>
            <input className="PlanBlockDeadline" type="date"
                   value={newPlanBlock.deadline.toISOString().split('T')[0]}
                   onChange={event => setDeadline(event.target.value)}>
            </input>
            <TextButton onClick={addPlanBlock} text="Добавить"/>
        </div>
    )
}


function PlanBlockRow({projectId, planBlock}: PlanBlockProps) {
    const [developer, setDeveloper] = useState<Worker>()
    const navigate = useNavigate()

    useEffect(() => {
        axios.get<Worker>(`http://localhost:8000/workers/${planBlock.developer_id}`)
            .then(response => setDeveloper(response.data))
            .catch(() => alert("Работника не существует"))
    }, []);

    function developerNavigate() {
        if (developer != undefined) {
            navigate(`/workers/${developer.id}`)
        }
    }

    function PlanBlockPageNavigate() {
        navigate(`/projects/${projectId}/plan_blocks/${planBlock.id}`)
    }

    return (
        <div className="PlanBlocksTableRow">
            <p className="Clickable" onClick={PlanBlockPageNavigate}>{planBlock.title}</p>
            <p className="Clickable" onClick={developerNavigate}>
                {developer ? developer.username : planBlock.developer_id}
            </p>
            <p>{(new Date(planBlock.deadline.toString())).toDateString()}</p>
        </div>
    )
}


function PlanBlocksDropList({projectId}: Props) {
    const [planBlocks, setPlanBlocks] = useState<PlanBlock[]>([])
    // const [active, setActive] = useState(false)
    const [searchActive, setSearchActive] = useState(false)


    useEffect(() => {
        axios.get<PlanBlock[]>(`http://localhost:8000/projects/${projectId}/plan_blocks`)
            .then(response => setPlanBlocks(response.data))
    }, [])
    function addPlanBlockForm() {
        setSearchActive(!searchActive)
    }

    return (
        <div className="PlanBlocksDropList">
            <DropListHeader title="Блоки планов" onClick={addPlanBlockForm} />
            {
                searchActive ? <PlanBlockForm projectId={projectId} /> : (<></>)
            }
            <div className="PlanBlocksTable">
                <div className="PlanBlocksTableHead">
                    <p>Название блока</p>
                    <p>Разработчик</p>
                    <p>Дедлайн</p>
                </div>
                <div className="PlanBlocksTableBody">
                {
                    planBlocks.map(planBlock =>
                        <PlanBlockRow planBlock={planBlock} projectId={projectId} key={planBlock.id}/>
                    )
                }
                </div>
            </div>
        </div>
    )
}

export default PlanBlocksDropList