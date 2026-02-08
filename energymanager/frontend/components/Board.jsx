import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

function Board() {
    const chartRef = useRef(null);
    let chartInstance = null;

    useEffect(() => {
        const myChartRef = chartRef.current.getContext("2d");
        
        const labels = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00'];

        chartInstance = new Chart(myChartRef, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Temperature (°C)",
                        data: [20, 21, 22, 21.5, 22, 23],
                        fill: false,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        tension: 0.1
                    },
                    {
                        label: "Person detected",
                        data: [1, 0, 1, 1, 0, 1],
                        fill: false,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        stepped: true,
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });

        return () => {
            chartInstance.destroy();
        }
    }, []);

    return (
        <main className="dash-main dash-container">
            <div style={{ position: 'relative', height: '40vh', width: '80vw' }}>
                <canvas ref={chartRef} />
            </div>
        </main>
    );
}

export { Board };