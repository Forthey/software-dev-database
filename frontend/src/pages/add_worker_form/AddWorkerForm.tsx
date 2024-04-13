// Stylesheets
import "./assets/AddWorkerForm.css"

// Modules
import {useNavigate} from "react-router";
import {ChangeEvent, useState} from "react";
import axios, {AxiosError, HttpStatusCode} from "axios";

// Interfaces
import {WorkerAdd} from "../../interfaces/worker.ts";


function AddWorkerForm() {
    let navigate = useNavigate()


    const [worker, setWorker] = useState<WorkerAdd>({
        specialization_code: 0,
        username: "",
        name: "",
        surname: "",
        email: "",
        level: 0
    })


    function setUsername(event: ChangeEvent<HTMLTextAreaElement>) {
        setWorker((previous) => ({...previous, username: event.target.value}))
    }

    function setName(event: ChangeEvent<HTMLTextAreaElement>) {
        setWorker((previous) => ({...previous, name: event.target.value}))
    }

    function setSurname(event: ChangeEvent<HTMLTextAreaElement>) {
        setWorker((previous) => ({...previous, surname: event.target.value}))
    }

    function setEmail(event: ChangeEvent<HTMLTextAreaElement>) {
        setWorker((previous) => ({...previous, email: event.target.value}))
    }

    function setSpecCode(event: ChangeEvent<HTMLSelectElement>) {
        setWorker((previous) => ({...previous, specialization_code: event.target.selectedIndex}))
    }

    function setLevel(event: ChangeEvent<HTMLSelectElement>) {
        setWorker((previous) => ({...previous, level: event.target.selectedIndex}))
    }


    async function addWorkerAndNavigateBack() {
            axios.post("http://localhost:8000/workers", worker).then(() => {
                navigate("/workers")
            }).catch((error: AxiosError) => {
                if (error.response == undefined) {
                    console.error("500: SERVICE UNAVAILABLE")
                } else {
                    if (error.response.status == HttpStatusCode.BadRequest) {
                        alert(`${worker.username} уже существует`)
                    }
                }
            })

    }


    return (
        <div>
            <div className="AddProjectForm">
                <div className="Title">Добавление работника</div>
                <textarea className="Username" placeholder="Username" value={worker.username} onChange={setUsername}/>
                <textarea className="Name" placeholder="Имя" value={worker.name} onChange={setName}/>
                <textarea className="Surname" placeholder="Фамилия" value={worker.surname} onChange={setSurname}/>
                <textarea className="Email" placeholder="Email" value={worker.email} onChange={setEmail}/>
                <select className="Specialization" onChange={setSpecCode}>
                    <option value="0">Разработчик</option>
                    <option value="1">Тестер</option>
                </select>
                <select className="Level" onChange={setLevel}>
                    <option value="0">Intern</option>
                    <option value="1">Junior</option>
                    <option value="2">Middle</option>
                    <option value="3">Senior</option>
                </select>
                <button className="SubmitButton" type="button" onClick={addWorkerAndNavigateBack}>Добавить</button>
            </div>
        </div>
    )
}

export default AddWorkerForm
