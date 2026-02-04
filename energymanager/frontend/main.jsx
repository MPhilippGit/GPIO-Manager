import 'vite/modulepreload-polyfill';
import "./scss/app.scss";
import "./scss/components/main.scss";
import { StrictMode } from 'react';
import { Sidebar } from './components/Sidebar.jsx';
import { Board } from './components/Board.jsx';
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <div className='dash'>
            <Sidebar />
            <Board />
        </div>
    </StrictMode>
);