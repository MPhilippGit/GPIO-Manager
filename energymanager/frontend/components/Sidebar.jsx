import "../scss/components/sidebar.scss";
import raspi from "../assets/raspi.svg"
import { Button } from "./Button";
import { viteUrl } from "../utils/vite-url";

const logoUrl = viteUrl(raspi);

function Sidebar() {
    return (
        <aside className="dash-sidebar dash-container">
            <img src={logoUrl} className="dash-sidebar_logo"/>
            <Button text="Temperatures" />
            <Button text="VOCs"/>
            <Button text="Humidity" />
        </aside>
    )
}

export { Sidebar };