import "./assets/Main.css"
import {useNavigate} from "react-router";


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
                <button className="Projects" type="button" onClick={projectsNavigate}>Проекты</button>
                <button className="Workers" type="button" onClick={workersNavigate}>Персонал</button>
            </div>
        </div>
    )
}

export default Main