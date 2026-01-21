// Import our custom CSS
import './scss/app.scss'
// Import all of Bootstrap’s JS
import * as bootstrap from 'bootstrap'
import { Chart } from 'chart.js/auto';

console.log('Vite läuft ✅');

async function fetchValuesFromSensors(endpoint) {
  const url = endpoint;
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error.message);
    return null;
  }
}

const fetchedData = fetchValuesFromSensors("api/temps");
