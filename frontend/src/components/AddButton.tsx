import "../assets/AddButton.css"
import {MouseEventHandler} from "react";

interface Props {
    onClick: MouseEventHandler
}

function AddButton({onClick}: Props) {
    return (
        <button className="AddButton" type="button" onClick={onClick}>
            <img className="AddIcon" src="/plus_icon.png" alt="Add"></img>
        </button>
    )
}

export default AddButton