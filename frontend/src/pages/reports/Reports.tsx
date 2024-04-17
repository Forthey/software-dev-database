// Stylesheets
import "./assets/Reports.css"

// My components
import ProjectQualityBlock from "./components/ProjectQualityBlock.tsx";
import WorkersReportDownload from "./components/WorkersReportDownload.tsx";
import ProjectsReportDownload from "./components/ProjectsReportDownload.tsx";


function Reports() {
    return(
        <div className="ReportsPage">
            <ProjectQualityBlock/>
            <WorkersReportDownload/>
            <ProjectsReportDownload/>
        </div>
    )
}


export default Reports