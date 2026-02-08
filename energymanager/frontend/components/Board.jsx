import Chart from 'chart.js/auto';
import { Line } from 'react-chartjs-2';
import "../scss/components/board.scss";

function Board() {
    const lineData = {
            labels: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
            datasets: [
                {
                    label: "Temperature (°C)",
                    data: [20, 21, 22, 21.5, 22, 23],
                    fill: false,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    tension: 0.1
                },
            ]
        }

    return (
        <main className="dash-main dash-container">
            <h2>Energy Monitor</h2>
            <div className='dash-main_graph'>
                <Line data={lineData} />
            </div>
        </main>
    );
}

export { Board };