import { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';
import { Line } from 'react-chartjs-2';
import { options } from '../utils/chart-options.js';
import "../scss/components/board.scss";
import { TimeFormatter } from '../utils/Timeformatter.js';


function Board({ graph }) {
    const [data, setData] = useState([]);

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
        const timestamp = new TimeFormatter(value.timestamp)
        return timestamp.getGraphFormat();
    })

    const lineData = {
            labels: labelValues,
            datasets: [
                {
                    label: "Temperature (°C)",
                    data: tempValues,
                    fill: false,
                    borderColor: 'rgb(185, 28, 62)',
                    tension: 0.1
                },
            ]
        }

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