import "../assets/Menu.css"
import MenuButton from "./MenuButton.tsx";
import {useNavigate} from "react-router";
import {useState} from "react";


function Menu() {
    const navigate = useNavigate()
    const [buttons, setButtons] = useState([
        {id: 1, text: "Главная", active: true, path: "/"},
        {id: 2, text: "Проекты", active: false, path: "/projects"},
        {id: 3, text: "Персонал", active: false, path: "/workers"},
        {id: 4, text: "Отчёты", active: false, path: "/reports"},
    ])

    function clicked(id: number) {
        setButtons(buttons.map(button => button.id == id ? {...button, active: true} : {...button, active: false}))
        const button = buttons.find(button => button.id == id)
        console.log(button)
        if (button !== undefined)
            navigate(button.path)
    }

    return (
        <div id="Menu">
            {
                buttons.map(button =>
                    <MenuButton key={button.id} id={button.id} text={button.text} active={button.active} onClick={clicked} />
                )
            }
        </div>
    )
}

export default Menu