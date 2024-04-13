import "../assets/DropListHeader.css"

import {MouseEventHandler} from "react";
import AddButton from "../../../components/AddButton.tsx";


interface Props {
    title: string
    onClick: MouseEventHandler
}

function DropListHeader({title, onClick}: Props) {
    return (
        <div className="DropListHeader">
            <p className="HeaderTitle">{title}</p>
            <AddButton onClick={onClick}/>
        </div>
    )
}

export default DropListHeader