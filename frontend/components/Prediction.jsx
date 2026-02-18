import "../scss/components/prediction.scss";
import { useState, useMemo } from "react";

function Prediction({ slope, intercept }) {
    const [xValue, setXValue] = useState("");

    // =========================
    // calculation
    // =========================
    const yValue = useMemo(() => {
        if (xValue === "") return "";
        let result = Math.round(slope * parseInt(xValue, 10) + intercept);
        if (result > 36) result = "36 (Maximalwert)"
        return result 
    }, [xValue, slope, intercept]);

    function handleChange(event) {
        const value = event.target.value;

        // Only allow numbers
        if (/^-?\d*$/.test(value)) {
            setXValue(value);
        }
    }
    return (
        <div className="prediction-wrapper">
            <div>
                <label htmlFor="x-input">Anzahl der Gäste:</label>
                <input
                    id="x-input"
                    type="text"
                    value={xValue}
                    onChange={handleChange}
                    placeholder="Ganze Zahl eingeben"
                />
            </div>

            <div style={{ marginTop: "1rem" }}>
                <label>Ermittelte Temperatur</label>
                <output>
                    ~ {yValue} °C
                </output>
            </div>
        </div>
    );
}

export { Prediction };
