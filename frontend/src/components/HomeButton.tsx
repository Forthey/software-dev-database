import "../assets/HomeButton.css"
import {useNavigate} from "react-router";


function HomeButton() {
    let navigate = useNavigate()

    function homeNavigate() {
        navigate("/")
    }

    return (
        <button className="HomeButton" onClick={homeNavigate}>
            <img src="/home_icon.png" alt="Home"></img>
        </button>
    )
}

export default HomeButton