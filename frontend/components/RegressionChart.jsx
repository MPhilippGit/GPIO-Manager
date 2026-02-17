import { useMemo, useState } from "react";
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

ChartJS.register(
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend,
    CategoryScale,
);

function RegressionChart({ data }) {
    const [ regressionData, setRegressiondata ] = useState([]);
    /**
     * data format expected:
     * [
     *   { x: 1, y: 10 },
     *   { x: 2, y: 15 },
     *   ...
     * ]
     */


    const fetchRegressionData = async (endpoint) => {
        try {
            const response = await fetch(endpoint);
            const result = await response.json();
            setRegressiondata(result)
        } catch (error) {
            console.error(error.message);
            setLatest([]);
        }
    };

    const extractTargetValues = (data) => {
        const resultData = []
        
        for (const row of data) {
            resultData.push({
                "x": row["voc_value"],
                "y": row["persons_estimated"]
            })
        }
        return resultData;
    }

    const chartData = useMemo(() => {
        fetchRegressionData("api/regression")

        const scatterData = extractTargetValues(regressionData);

        if (!scatterData || scatterData.length === 0) return null;

        // Calculate regression
        const regressionResult = regression.linear(
            data.map((point) => [point.x, point.y]),
        );

        const regressionPoints = data.map((point) => ({
            x: point.x,
            y: regressionResult.predict(point.x)[1],
        }));

        console.log(regressionPoints);

        return {
            datasets: [
                // Dataset 1: Raw Points
                {
                    type: "scatter",
                    label: "Measurements",
                    data: scatterData,
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
    }, [data]);

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

    return (
        <Scatter data={chartData} options={options} />
    )
}

export default RegressionChart;
