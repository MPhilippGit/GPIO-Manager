import 'vite/modulepreload-polyfill'
import { StrictMode } from 'react';
import { Sidebar } from './components/Sidebar.jsx';
import { Board } from './components/Board.jsx';
import { createRoot } from 'react-dom/client';
import "./scss/app.scss";

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <div className='dash'>
            <Sidebar />

        </div>
    </StrictMode>
);