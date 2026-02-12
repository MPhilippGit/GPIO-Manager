import { PATHS } from "../globals";

const options = {
    [PATHS.TEMP]: {
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
    [PATHS.HUMID]: {
        scales: {
            y: {
                suggestedMin: 0,
                suggestedMax: 100,
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
    [PATHS.VOC]: {
        scales: {
            y: {
                suggestedMin: 0,
                suggestedMax: 1,
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
    [PATHS.TEMP]: {
        label: "Temperature (°C)",
        fill: true,
        borderColor: "rgb(185, 28, 62)",
        tension: 0.1,
    },
    [PATHS.HUMID]: {
        label: "Restfeuchte (rH)",
        fill: true,
        borderColor: "rgb(33, 114, 130)",
        tension: 0.1,
    },
    [PATHS.VOC]: {
        label: "VOC Konzentration (ppm)",
        fill: true,
        borderColor: "rgb(181, 149, 32)",
        tension: 0.1,
    },
};

export { options, datasets };
