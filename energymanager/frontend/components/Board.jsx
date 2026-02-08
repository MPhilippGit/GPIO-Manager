import { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';
import { Line } from 'react-chartjs-2';
import { tempOptions } from '../utils/chart-options.js';
import "../scss/components/board.scss";


function Board() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchSensorData("api/temps");
    }, [])

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
    const labelValues = data.map(value => value.timestamp)

    const lineData = {
            labels: labelValues,
            datasets: [
                {
                    label: "Temperature (°C)",
                    data: tempValues,
                    fill: false,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    tension: 0.1
                },
            ]
        }
    
    const graphOptions = {
        maintainAspectRatio: false,
        responsive: true,
    }

    return (
        <main className="dash-main dash-container">
            <h2>Energy Monitor</h2>
            <div className='dash-main_graph'>
                <Line data={lineData} options={tempOptions} />
            </div>
        </main>
    );
}

export { Board };