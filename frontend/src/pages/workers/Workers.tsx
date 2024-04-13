import WorkersList from "./components/WorkersList.tsx";
import "./assets/Workers.css"
import AddButton from "../../components/AddButton.tsx";
import {useNavigate} from "react-router";


function Workers() {
    let navigate = useNavigate()

    function addWorkerNavigate() {
        navigate("add")
    }

    return (
        <div className="WorkersPage">
            <AddButton onClick={addWorkerNavigate}/>
            <WorkersList />
        </div>
    )
}

export default Workers