import { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';
import { Line } from 'react-chartjs-2';
import { options, datasets } from '../utils/chart-options.js';
import { TimeFormatter } from '../utils/Timeformatter.js';
import "../scss/components/board.scss";


function Board({ graph }) {
    const [data, setData] = useState([]);

    const lineData = {
        datasets: []
    };
    const chartDataset = datasets[graph]

    useEffect(() => {
        fetchSensorData(graph);
    }, [graph])

    const fetchSensorData = async (endpoint) => {
        try {
            const response = await fetch(endpoint);
            const result = await response.json();
            setData(result)
        }
        catch (error) {
            console.error(error.message)
            setData({})
        }
    }
    const tempValues = data.map(value => value.measurement)
    const labelValues = data.map(value => {
        if (!value) return null;
        const timestamp = new TimeFormatter(value.timestamp)
        return timestamp.getGraphFormat();
    })

    chartDataset.data = tempValues;

    lineData.datasets.push(chartDataset);
    lineData.labels = labelValues;

    return (
        <main className="dash-main dash-container">
            <h2>Energy Monitor</h2>
            <div className='dash-main_graph'>
                <Line data={lineData} options={options[graph]} />
            </div>
        </main>
    );
}

export { Board };