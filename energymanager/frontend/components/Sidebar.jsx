function Sidebar() {
    return (
        <aside className="dash-sidebar dash-container">
            <img src="dist/raspi.svg" className="dash-sidebar_logo" />
            <button className="button-primary">Temperatures</button>
            <button className="button-primary">Humidity</button>
            <button className="button-primary">Pressure</button>
        </aside>
    )
}

export { Sidebar };