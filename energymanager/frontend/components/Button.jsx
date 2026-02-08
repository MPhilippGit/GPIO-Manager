import "../scss/components/buttons.scss";

function Button({ text }) {
    return (
        <button className="button-primary">
            {text}
        </button>
    )
}

export { Button };