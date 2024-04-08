import "./App.css"
import {Route, Routes} from "react-router-dom"

import Projects from "./pages/projects/Projects.tsx"
import AddProjectForm from "./pages/add_project_form/AddProjectForm.tsx"
import Main from "./pages/main/Main.tsx";


function App() {
  // const [count, setCount] = useState(0)
  return (
      <Routes>
          <Route path="/" Component={Main}></Route>
          <Route path="/projects" Component={Projects}></Route>
          <Route path="/projects/add" Component={AddProjectForm}></Route>
      </Routes>
  )
}

export default App
