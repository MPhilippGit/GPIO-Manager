import { useEffect, useMemo, useState } from "react";
import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend,
    CategoryScale,
} from "chart.js";
import { Scatter } from "react-chartjs-2";
import regression from "regression";
import { PredictionHelper } from "../utils/prediction";

ChartJS.register(
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend,
    CategoryScale,
);

function RegressionChart({ prediction }) {
    const [ regressionModelData, setRegressionModelData ] = useState([])

    const fetchRegression = async () => {
        try {
            const response = await fetch(prediction);
            console.log(response.ok)
            const result = await response.json();
            setRegressionModelData(result)
        } catch (error) {
            console.error(error.message);
            setRegressionModelData([]);
        }
    }

    useEffect(() => {
        fetchRegression(prediction);
    }, [prediction]);

    const getScatteredData = () => {
        return regressionModelData.data.map(entry => [entry.voc, entry.target]);
    }

    const getRegressionHandler = () => {
        return new PredictionHelper(regressionModelData.model.slope, regressionModelData.model.intercept)
    }

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: "top",
            },
        },
        scales: {
            x: {
                type: "linear",
                title: {
                    display: true,
                    text: "X Axis",
                },
            },
            y: {
                title: {
                    display: true,
                    text: "Y Axis",
                },
            },
        },
    };

    const data = {
        datasets: [
            // Dataset 1: Raw Points
            {
                type: "scatter",
                data: regressionModelData.data && getScatteredData(),
                label: "Measurements",
                backgroundColor: "rgba(54, 162, 235, 0.8)",
                pointRadius: 4,
            },

            // Dataset 2: Regression Line
            {
                type: "line",
                label: "Linear Regression",
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 2,
                fill: false,
                tension: 0,
                pointRadius: 0,
            },
        ],
    };

    return (
        <Scatter data={data} options={options} />
    )
}

export default RegressionChart;
