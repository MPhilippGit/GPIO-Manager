import 'vite/modulepreload-polyfill';
import "./scss/app.scss";
import "./scss/components/main.scss";
import { viteUrl } from './utils/vite-url.js';
import { StrictMode } from 'react';
import { Sidebar } from './components/Sidebar.jsx';
import { Board } from './components/Board.jsx';
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
console.log(import.meta.env.DEV)
root.render(
    <StrictMode>
        <div className='dash'>
            <Sidebar />
            <Board />
        </div>
    </StrictMode>
);