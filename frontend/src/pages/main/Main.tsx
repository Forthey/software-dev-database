import "./assets/Main.css"
import {useNavigate} from "react-router";
import TextButton from "../../components/TextButton.tsx";


function Main() {
    let navigate = useNavigate()

    function projectsNavigate() {
        navigate("/projects")
    }

    function workersNavigate() {
        navigate("/workers")
    }

    return (
        <div className="Main">
            <div className="CompanyName">Forthey Group</div>
            <div className="About">Мы занимаемся разработкой B2B программного обеспечения уже 5 недель. Наш персонал включает в себя отборных бездарей, а наши проекты покоряют самые днища возможностей</div>
            <div className="Buttons">
                <TextButton text="Проекты" onClick={projectsNavigate} />
                <TextButton text="Персонал" onClick={workersNavigate} />
            </div>
        </div>
    )
}

export default Main