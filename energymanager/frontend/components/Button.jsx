import "../scss/components/buttons.scss";
import { Icon } from "./Icon";

function Button({ text, icon }) {
    const buttonIcon = icon ? <Icon name={icon} size={18} /> : "";

    return (
        <button className="button-primary">
            {buttonIcon}
            {text}
        </button>
    )
}

export { Button };