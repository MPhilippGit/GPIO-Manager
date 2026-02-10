import "../scss/components/buttons.scss";
import { Icon } from "./Icon";

function Button({ text, icon, setGraph }) {
    const buttonIcon = icon ? <Icon name={icon} size={18} /> : "";

    const changeGraph = () => {
        setGraph("api/humids")
    }

    return (
        <button onClick={changeGraph} className="button-primary">
            {buttonIcon}
            {text}
        </button>
    )
}

export { Button };