// Stylesheets
import "../assets/RestoreButton.css"

// Modules
import {MouseEventHandler} from "react";


interface Props {
    onClick: MouseEventHandler
}

function RestoreButton({onClick}: Props) {
    return (
        <div className="RestoreButton" onClick={onClick}>
            <img className="RestoreIcon" src="/restore.png" alt="Restore"/>
        </div>
    )
}

export default RestoreButton