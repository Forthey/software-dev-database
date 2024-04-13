// Stylesheets
import "./assets/AddProjectForm.css"

// Modules
import {useNavigate} from "react-router";
import {ChangeEvent, useState} from "react";
import axios, {AxiosError, HttpStatusCode} from "axios";

// Interfaces
import {ProjectAdd} from "../../interfaces/project.ts";


function AddProjectForm() {
    const navigate = useNavigate()
    const [project, setProject] = useState<ProjectAdd>({
        name: "",
        description: ""
    })


    function addProjectAndNavigateBack() {
        axios.post("http://localhost:8000/projects", project).then(() => {
            navigate("/projects")
        }).catch((error: AxiosError) => {
            if (error.response == undefined) {
                console.error("500: SERVICE UNAVAILABLE")
            } else {
                if (error.response.status == HttpStatusCode.BadRequest) {
                    alert(`Проект \"${project.name}\" уже существует`)
                }
            }
        })
    }

    function setName(event: ChangeEvent<HTMLTextAreaElement>) {
        setProject((previous) => ({...previous, name: event.target.value}))
    }

    function setDescription(event: ChangeEvent<HTMLTextAreaElement>) {
        setProject((previous) => ({...previous, description: event.target.value}))
    }


    return (
        <div>
            <div className="AddProjectForm">
                <div className="Title">Добавление проекта</div>
                <textarea className="Name" placeholder="Имя проекта" onChange={setName}>{project.name}</textarea>
                <textarea className="Description" placeholder="Описание проекта" onChange={setDescription}>{project.description}</textarea>
                <button className="SubmitButton" type="button" onClick={addProjectAndNavigateBack}>Добавить</button>
            </div>
        </div>
    )
}

export default AddProjectForm
