import { PATHS } from "../globals";
import { Button } from "./Button";

function GraphInterface({ setGraph }) {
    return (
        <div className="dash-sidebar_interface">
            <Button
                className="btn-sidebar"
                target={PATHS.TEMP}
                setGraph={setGraph}
                text="Temperatures"
                icon="thermometer"
            />
            <Button
                className="btn-sidebar"
                target={PATHS.VOC}
                setGraph={setGraph}
                text="VOCs"
                icon="spray-can"
            />
            <Button
                className="btn-sidebar"
                target={PATHS.HUMID}
                setGraph={setGraph}
                text="Humidity"
                icon="bubbles"
            />
        </div>
    );
}

export { GraphInterface }