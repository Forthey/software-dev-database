// Stylesheets
import "../assets/WorkersReportDownload.css"

// Modules
import axios from "axios";

// My components
import DownloadButton from "../../../components/DownloadButton.tsx";

function WorkersReportDownload() {
    function onDownloadRequest() {
        axios.get("http://localhost:8000/reports/workers", {responseType: "blob"})
            .then(response => {
            const url = window.URL.createObjectURL(
                response.data,
            );
            const link = document.createElement('a');

            link.href = url;

            link.setAttribute(
                'download',
                `workers.md`,
            );

            // Append to html link element page
            document.body.appendChild(link);

            // Start download
            link.click();
            // Clean up and remove the link

            if (link.parentNode == null) {
                return
            }
            link.parentNode.removeChild(link);
        })
    }

    return (
        <div className="WorkersReportDownload">
            <p>Список персонала (markdown)</p>
            <DownloadButton onClick={onDownloadRequest}/>
        </div>
    )
}

export default WorkersReportDownload