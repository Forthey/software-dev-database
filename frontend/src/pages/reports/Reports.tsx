import "./assets/Reports.css"

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import {Bar}  from "react-chartjs-2"
import {useEffect, useState} from "react";
import axios from "axios";
import {ProjectQuality} from "../../interfaces/project.ts";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

export const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top' as const,
        },
        title: {
            display: true,
            text: 'Диаграмма по завершенным проектам',
        },
    },
};


function Reports() {
    // const [labels, setLabels] = useState<string[]>([])
    const [data, setData] = useState({
        labels: [""],
        datasets: [
            {
                label: 'Проекты',
                data: [0],
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderRadius: 10
            }
        ],
    })

    useEffect(() => {
        axios.get<ProjectQuality[]>("http://localhost:8000/quality")
            .then(response => {
                setData({
                    labels: response.data.map(project => project.project_name),
                    datasets: [
                        {
                            label: 'Качество разработки',
                            data: response.data.map(project => project.quality),
                            backgroundColor: 'rgba(255, 99, 132, 0.5)',
                            borderRadius: 10
                        }
                    ],
                })
            })
    }, []);

    return(
        <div className="ReportsPage">
            <Bar options={options} data={data} />
        </div>
    )
}


export default Reports