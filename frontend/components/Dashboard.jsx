import "../scss/components/dashboard.scss";
import { Icon } from "./Icon";
import { useEffect, useState } from "react";

function Measurement({ value, unit, icon }) {
    const [ latest, setLatest ] = useState([]);

    useEffect(() => {
        fetchLatest("api/latest")
    }, [])

    const fetchLatest = async (endpoint) => {
        try {
            const response = await fetch(endpoint);
            console.log(response, "hallo")
            const result = await response.json();
            setLatest(result);
        } catch (error) {
            console.error(error.message);
            setLatest([]);
        }
    };
    console.log(latest)

    return (
        <div>
            {icon}
            {value}
            <span>{unit}</span>
        </div>
    )
}

function Dashboard() {
    return (
        <div className="dash-container dash-board">
            <h1>Hello</h1>
            <div className="dash-board_measurements">
                <Measurement 
                    value={"Blub"}
                    unit={"hPa"}
                    icon={<Icon name="bubbles" color="white" size={48} />}
                />
            </div>
        </div>
    )
}

export { Dashboard };