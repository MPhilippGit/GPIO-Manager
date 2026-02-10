const options = {
    "api/temps": {
        scales: {
            y: {
                suggestedMin: 15,
                suggestedMax: 30,
            },
        },
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        size: 22,
                    },
                },
            },
        },
    },
};

const datasets = {
    "api/temps": {
        label: "Temperature (°C)",
        fill: true,
        borderColor: "rgb(185, 28, 62)",
        tension: 0.1,
    },
    "api/humids": {
        label: "Restfeuchte (rH)",
        fill: true,
        borderColor: "rgb(33, 114, 130)",
        tension: 0.1,
    },
    "api/vocs": {
        label: "VOC Konzentration (ppm)",
        fill: true,
        borderColor: "rgb(181, 149, 32)",
        tension: 0.1,
    },
};

export { options, datasets };
