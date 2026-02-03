import 'vite/modulepreload-polyfill'
import { StrictMode } from 'react';
import { Button } from './Button.jsx';
import { createRoot } from 'react-dom/client';
import "./main.css";

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <h1>Check 12</h1>
        <Button />
    </StrictMode>
);