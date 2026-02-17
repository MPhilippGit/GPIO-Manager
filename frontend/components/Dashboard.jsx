import "../scss/components/dashboard.scss";
import { Icon } from "./Icon";
import { useEffect, useState } from "react";
import RegressionChart from "./RegressionChart";

function Measurement({ value, unit, icon, refreshKey, prediction }) {
    return (
        <div key={refreshKey} className={prediction ? "latest_prediction": "latest_box"}>
            {prediction && <p>{prediction}</p>}
            {icon}
            <span>
                {value} {unit}
            </span>
        </div>
    )
}

function Refresher ({ onClick }) {
    return (
        <button onClick={onClick} className="btn-primary btn-refresh">
            <Icon name="refresh-cw"/>
            Refresh
        </button>
    )
}

function Dashboard() {
    const [refreshKey, setRefreshKey] = useState(0);
    const [latest, setLatest] = useState([]);

    useEffect(() => {
        fetchLatest("api/all")
    }, [refreshKey])

    const refresh = () => {
        setRefreshKey(refreshKey + 1)
    }

    const fetchLatest = async (endpoint) => {
        try {
            const response = await fetch(endpoint);
            const result = await response.json();
            setLatest(result);
        } catch (error) {
            console.error(error.message);
            setLatest([]);
        }
    };

    return (
        <div className="dash-container dash-board">
            <div className="dash-board_measurements">
                <div className="dash-board_regression">
                    <h4>Regression</h4>
                    <div className="dash-board_regression-graph">
                        <RegressionChart
                            prediction={"predict/guests"}
                        />
                    </div>
                    <div className="dash-board_regression-predictions">
                        <h4>Predictions</h4>
                        <Measurement
                            prediction={"Vorhergesagter Tempearaturwert:"}
                            refreshKey={refreshKey}
                            value={latest.temperature}
                            unit={"°C"}
                        />
                        <Measurement
                            prediction={"R-Wert"}
                            refreshKey={refreshKey}
                            value={latest.humidity}
                            unit={"rH[%]"}
                        />
                    </div>
                </div>
                <div className="latest">
                    <h4>Messwerte</h4>
                    <Measurement
                        refreshKey={refreshKey}
                        value={latest.pressure}
                        unit={"hPa"}
                        icon={<Icon name="circle-gauge" size={32} />}
                    />
                    <Measurement
                        refreshKey={refreshKey}
                        value={latest.humidity}
                        unit={"rH[%]"}
                        icon={<Icon name="bubbles" size={32} />}
                    />
                    <Measurement
                        refreshKey={refreshKey}
                        value={latest.voc}
                        unit={"Ohm"}
                        icon={<Icon name="spray-can" size={32} />}
                    />
                    <Measurement
                        refreshKey={refreshKey}
                        value={latest.temperature}
                        unit={"°C"}
                        icon={
                            <Icon name="thermometer" color="white" size={32} />
                        }
                    />
                    <div className="latest_interface">
                        <Refresher onClick={refresh} />
                    </div>
                </div>
            </div>
        </div>
    );
}

export { Dashboard };