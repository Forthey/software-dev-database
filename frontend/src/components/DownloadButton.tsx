// Stylesheets
import "../assets/DownloadButton.css"

// Modules
import {MouseEventHandler} from "react";


interface Props {
    onClick: MouseEventHandler
}

function DownloadButton({onClick}: Props) {
    return (
        <div className="DownloadButton" onClick={onClick}>
            <img className="DownloadIcon" src="/download.png" alt="Download"/>
        </div>
    )
}

export default DownloadButton