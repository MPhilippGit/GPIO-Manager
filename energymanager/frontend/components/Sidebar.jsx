import "../scss/components/sidebar.scss";


function Sidebar() {
    return (
        <aside className="dash-sidebar dash-container">
            <button className="button-primary">Temperatures</button>
            <button className="button-primary">Humidity</button>
            <button className="button-primary">Pressure</button>
        </aside>
    )
}

export { Sidebar };