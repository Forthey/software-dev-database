import "./App.css"
import {Route, Routes} from "react-router-dom"

import Projects from "./pages/projects/Projects.tsx"
import Workers from "./pages/workers/Workers.tsx";
import AddProjectForm from "./pages/add_project_form/AddProjectForm.tsx"
import AddWorkerForm from "./pages/add_worker_form/AddWorkerForm.tsx";
import Main from "./pages/main/Main.tsx";
import ProjectPage from "./pages/project/ProjectPage.tsx";
import Menu from "./components/Menu.tsx";
import WorkerPage from "./pages/worker/WorkerPage.tsx";


function App() {
  // const [count, setCount] = useState(0)
  return (
      <>
      <Menu />
      <Routes>
          <Route path="/" Component={Main}></Route>
          <Route path="/projects" Component={Projects}></Route>
          <Route path="/projects/add" Component={AddProjectForm}></Route>
          <Route path="/workers" Component={Workers}></Route>
          <Route path="/workers/add" Component={AddWorkerForm}></Route>
          <Route path="/projects/:id" Component={ProjectPage}></Route>
          <Route path="/workers/:id" Component={WorkerPage}></Route>
      </Routes>
      </>
  )
}

export default App
