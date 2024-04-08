import "../assets/AddButton.css"
import {useNavigate} from "react-router";

function AddButton() {
    let navigate = useNavigate()

    function addProjectNavigate() {
        navigate("add")
    }

    return (
        <button className="AddButton" type="button" onClick={addProjectNavigate}>
            <img className="AddIcon" src="plus_icon.png" alt="Add"></img>
        </button>
    )
}

export default AddButton