import "../assets/TextButton.css"
import {MouseEventHandler} from "react";

interface Props {
    text: string
    onClick: MouseEventHandler
}


function TextButton({text, onClick}: Props) {
    return (
        <button className="DefaultButton" onClick={onClick}>
            {text}
        </button>
    )
}


export default TextButton