import "../assets/DeleteButton.css"
import {MouseEventHandler} from "react";

interface Props {
    onClick: MouseEventHandler
}

function DeleteButton({onClick}: Props) {
    return (
        <div className="DeleteButton" onClick={onClick}>
            <img className="DeleteIcon" src="/trash.png" alt="Del"/>
        </div>
    )
}

export default DeleteButton