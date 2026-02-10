import "../scss/components/sidebar.scss";
import raspi from "../assets/raspi.svg"
import { Button } from "./Button";
import { PATHS } from "../globals";
import { viteUrl } from "../utils/vite-url";

const logoUrl = viteUrl(raspi);

function Sidebar({ setGraph }) {
    return (
        <aside className="dash-sidebar dash-container">
            <img src={logoUrl} className="dash-sidebar_logo"/>
            <Button target={PATHS.TEMP} setGraph={setGraph} text="Temperatures" icon="thermometer" />
            <Button target={PATHS.VOC} setGraph={setGraph} text="VOCs" icon="spray-can" />
            <Button target={PATHS.HUMID} setGraph={setGraph} text="Humidity" icon="bubbles" />
        </aside>
    )
}

export { Sidebar };