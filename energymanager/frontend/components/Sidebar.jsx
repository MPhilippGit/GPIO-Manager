import "../scss/components/sidebar.scss";


function Sidebar() {
    return (
        <aside className="dash-sidebar">
            <button className="button-primary">Temperatures</button>
            <button className="button-primary">Humidity</button>
        </aside>
    )
}

export { Sidebar };