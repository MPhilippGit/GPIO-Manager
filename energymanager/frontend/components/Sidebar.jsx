import "../scss/components/sidebar.scss";
import logo from '../assets/raspi.svg';


function Sidebar() {
    return (
        <aside className="dash-sidebar dash-container">
            <img src={logo} />
            <button className="button-primary">Temperatures</button>
            <button className="button-primary">Humidity</button>
            <button className="button-primary">Pressure</button>
        </aside>
    )
}

export { Sidebar };