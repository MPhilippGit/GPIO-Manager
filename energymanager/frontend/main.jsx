import 'vite/modulepreload-polyfill';
import "./scss/app.scss";
import "./scss/components/main.scss";
import { viteUrl } from './utils/vite-url.js';
import { StrictMode, useState } from 'react';
import { Sidebar } from './components/Sidebar.jsx';
import { Board } from './components/Board.jsx';
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <App />
    </StrictMode>
);

function App() {
    const [ graph, setGraph ] = useState("api/temps")

    return (
        <div className='dash'>
            <Sidebar graph={graph} setGraph={setGraph} />
            <Board graph={graph} setGraph={setGraph} />
        </div>
    )
}