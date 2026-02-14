import "../scss/components/dashboard.scss";
import { Icon } from "./Icon";
import { useEffect, useState } from "react";

function Measurement({ value, unit, icon }) {
    

    return (
        <div className="latest_box">
            {icon}
            {value}
            <span>{unit}</span>
        </div>
    )
}

function Refresher () {
    return (
        <button className="btn-primary">
            <Icon name="refresh-cw"/>
        </button>
    )
}

function Dashboard() {
    const [refreshKey, setRefreshKey] = useState(0);
    const [latest, setLatest] = useState([]);

    useEffect(() => {
        fetchLatest("api/all")
    }, [refreshKey])

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
            <h1>Hello</h1>
            <div className="dash-board_measurements">
                <div className="latest">
                    <Measurement 
                        value={latest.pressure}
                        unit={"hPa"}
                        icon={<Icon name="circle-gauge" color="black" size={32} />}
                    />
                    <Measurement 
                        value={latest.humidity}
                        unit={"rH[%]"}
                        icon={<Icon name="bubbles" color="black" size={32} />}
                    />
                    <Measurement 
                        value={latest.voc}
                        unit={"Ohm"}
                        icon={<Icon name="spray-can" color="black" size={32} />}
                    />
                    <Measurement 
                        value={latest.temperature}
                        unit={"°C"}
                        icon={<Icon name="thermometer" color="black" size={32} />}
                    />
                    <div>
                        <Refresher onClick={() => setRefreshKey(k => k+1)} />
                    </div>
                </div>
            </div>
        </div>
    )
}

export { Dashboard };