import "../scss/components/buttons.scss";
import { PATHS } from "../globals";
import { Icon } from "./Icon";

function Button({ target, text, icon, setGraph }) {
    const buttonIcon = icon ? <Icon name={icon} size={18} /> : "";

    const changeGraph = (e) => {
        const endpoint = e.target.dataset["target"]
        setGraph(endpoint)
    }

    return (
        <button data-target={target} onClick={changeGraph} className="button-primary">
            {buttonIcon}
            {text}
        </button>
    )
}

export { Button };