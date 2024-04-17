// Stylesheets
import "../assets/PlanBlockDev.css"

// Modules
import {useNavigate} from "react-router";
import axios from "axios";

// My components
import TextButton from "../../../components/TextButton.tsx";
import {useState} from "react";

// Interfaces
import {Worker} from "../../../interfaces/worker.ts";
import {levelToStr} from "../../../interfaces/enums.ts";


interface Props {
    project_id: number,
    plan_block_id: number
}

function PlanBlockDev({project_id, plan_block_id}: Props) {
    const navigate = useNavigate()
    const [testerUsername, setTesterUsername] = useState<string>("")
    const [testers, setTesters] = useState<Worker[]>([])

    function sendToTest() {
        const tester = testers.find(tester => tester.username == testerUsername)
        if (tester == undefined) {
            alert("Что-то пошло не так...")
            return
        }
        axios.post(`http://localhost:8000/projects/${project_id}/plan_blocks/${plan_block_id}/tests/${tester.id}`)
            .then(() => navigate(0))
            .catch(() => alert("Что-то пошло не так..."))
    }

    function setTestersDatalist(usernameMask: string) {
        setTesterUsername(usernameMask)
        axios.get<Worker[]>(`http://localhost:8000/workers/search/tester/`,
            {params: {username_mask: usernameMask}})
            .then(response => setTesters(response.data))
    }


    return (
        <div className="PlanBlockDev">
            <p>Тестирование</p>
            <div className="SendToTestForm">
                <input className="SearchTesters" placeholder="Username тестировщика"
                       onChange={event => setTestersDatalist(event.target.value)}
                       onFocus={event => setTestersDatalist(event.target.value)}
                       list="TestersDataList"
                />
                <datalist id="TestersDataList">
                    {
                        testers.filter(tester => tester.fire_date == null).map(tester =>
                            <option key={tester.id} value={tester.username}>
                                {`${tester.surname} ${tester.name}\n${levelToStr[tester.level]}`}
                            </option>
                        )
                    }
                </datalist>
                <TextButton text="Отправить на тестировку" onClick={sendToTest} />
            </div>
        </div>
    )
}

export default PlanBlockDev