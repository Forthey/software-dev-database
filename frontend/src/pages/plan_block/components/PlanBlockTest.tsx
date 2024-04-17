// Stylesheets
import "../assets/PlanBlockTest.css"

// Modules
import {useState} from "react";

// My components
import TextButton from "../../../components/TextButton.tsx";
import AddButton from "../../../components/AddButton.tsx";

// Enums and interfaces
import {BlockBugAdd} from "../../../interfaces/plan_block.ts";
import {BugCategory, bugCategoryToStr} from "../../../interfaces/enums.ts";
import axios from "axios";
import {useNavigate} from "react-router";
import DeleteButton from "../../../components/DeleteButton.tsx";


interface Props {
    project_id: number,
    plan_block_id: number,
    tester_id: number | undefined
}

interface BugFieldProps {
    index: number
    bug: BlockBugAdd
    onTitleChange: Function
    onCategoryChange: Function
    onDelete: Function
}

function BugField({index, onTitleChange, onCategoryChange, bug, onDelete}: BugFieldProps) {
    return (
        <div className="BugField">
            <input className="BugTitle" placeholder="Что не так?"
                   onChange={event => onTitleChange(index, event.target.value)}
            />
            <select className="BugCategory" onChange={event => onCategoryChange(index, event.target.value)}>
                <option value={BugCategory.minor}>{bugCategoryToStr[BugCategory.minor]}</option>
                <option value={BugCategory.serious}>{bugCategoryToStr[BugCategory.serious]}</option>
                <option value={BugCategory.showstopper}>{bugCategoryToStr[BugCategory.showstopper]}</option>
            </select>
            <DeleteButton onClick={() => onDelete(index)} />
        </div>
    )
}


function PlanBlockTest({project_id, plan_block_id, tester_id}: Props) {
    const navigate = useNavigate()
    const [bugs, setBugs] = useState<BlockBugAdd[]>([])

    function setBugTitle(id: number, title: string) {
        setBugs(bugs.map(
            (bug, index) => id != index ? bug : {...bug, title: title}
        ))
    }

    function setBugCategory(id: number, category: BugCategory) {
        setBugs(bugs.map(
            (bug, index) => id != index ? bug : {...bug, category: category}
        ))
    }

    function addBugField() {
        if (tester_id != undefined) {
            const newBug: BlockBugAdd = {
                title: "",
                tester_id: tester_id,
                block_id: plan_block_id,
                category: BugCategory.minor
            }

            setBugs([...bugs, newBug])
        }
    }

    function deleteBugField(i: number) {
        setBugs(bugs.filter(((bug, index) => index != i)))
    }

    function submitBugs() {

        for (const bug of bugs) {
            if (bug.title.length < 1) {
                alert("Заполните все поля")
                return
            }
        }

        axios.post<BlockBugAdd[]>(`http://localhost:8000/projects/${project_id}/plan_blocks/${plan_block_id}/bugs`,
            bugs, { params: { tester_id: tester_id } })
            .then(() => navigate(0))
            .catch(() => alert("Что-то пошло не так..."))
    }

    return (
        <div className="PlanBlockTest">
            <div className="BlockBugAdd">
            {
                bugs.map((bug, index) => <BugField key={index} index={index} bug={bug}
                                                    onTitleChange={setBugTitle}
                                                    onCategoryChange={setBugCategory}
                                                    onDelete={deleteBugField}
                />)
            }
            </div>
            <AddButton onClick={addBugField}/>
            <TextButton text="Отправить" onClick={submitBugs}/>
        </div>
    )
}

export default PlanBlockTest