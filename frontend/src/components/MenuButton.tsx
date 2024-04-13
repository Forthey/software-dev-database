import "../assets/MenuButton.css"

interface Props {
    id: number
    text: string
    active: boolean
    onClick: Function
}

function MenuButton({id, text, active, onClick}: Props) {


    function clicked() {
        onClick(id)
    }

    return (
        <div className={`MenuButton${active ? " Active" : ""}`} onClick={clicked}>
            {text}
        </div>
    )
}

export default MenuButton