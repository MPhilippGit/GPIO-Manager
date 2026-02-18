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

    useEffect(() => {
        fetchRegression(prediction);
    }, [prediction]);

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

    const getScatteredData = () => {
        return regressionModelData.data.map(entry => [entry.source, entry.target]);
    }

    const getRegressionLine = () => {
        const handler = new PredictionHelper(regressionModelData.model.slope, regressionModelData.model.intercept)
        return handler.getXYValues(regressionModelData.data.map(entry => entry.source));
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
                data: regressionModelData.data && getRegressionLine(),
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 2,
                fill: false,
                tension: 0,
                pointRadius: 0,
            },
        ],
    };

    return (
        <>
            <div className="dash-board_regression-predictions">
                <h4>Regressionsmodell</h4>
                <Scatter data={data} options={options} />
                
            </div>
        </>
    );
}

export default RegressionChart;
