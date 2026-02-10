import "../scss/components/sidebar.scss";
import raspi from "../assets/raspi.svg"
import { Button } from "./Button";
import { viteUrl } from "../utils/vite-url";

const logoUrl = viteUrl(raspi);

function Sidebar({ setGraph }) {
    return (
        <aside className="dash-sidebar dash-container">
            <img src={logoUrl} className="dash-sidebar_logo"/>
            <Button text="Temperatures" icon="thermometer" />
            <Button text="VOCs" icon="spray-can" />
            <Button setGraph={setGraph} text="Humidity" icon="bubbles" />
        </aside>
    )
}

export { Sidebar };