import "../assets/TransferButton.css"

import {MouseEventHandler} from "react";

interface Props {
    onClick: MouseEventHandler
}

function TransferButton({onClick}: Props) {
    return (
        <div className="TransferButton" onClick={onClick}>
            <img className="TransferIcon" src="/transfer.png" alt="Transfer"/>
        </div>
    )
}

export default TransferButton
