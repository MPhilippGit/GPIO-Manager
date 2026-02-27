# Projektdokumentation

## Einleitung

### Projektbeteiligte:
- Philipp Müller
- Cedric Hintzen

### Anforderungsprofil:
- Erfassung von Sensordaten:
    - BME680
    - RCWL-0516
- Automatisierte Datenpflege:
    - Auslesen der erfassten Daten alle 5 Minuten
    - Daten, welche älter sind als 30 Tage werden automatisiert gelöscht
- Weboberfläche mit Anzeige der aktuellen Daten
- Regressionsanalyse
- Fehlerlogs (Datenbank + Sensorausfälle)

### Verwendete Technologien zur Umsetzung des Anforderungsprofils:
- Systemarchitektur:
    - mariadb - Datenbank
    - Apache - Webserver
- Programmiersprachen:
    - Python v3.13 (Backend, Sensordaten, Datenbanktransaktionen, Regression)
    - JavaScript ES6+ (UI, Graphische Darstellung)
- Python Bibliotheken:
    - scikit-learn v1.8.0 - Regressionsanalyse
    - bme680 v2.0.0 - Sensorwerterfassung (bme680)
    - gpiozero v2.0.1 - Sensorwerterfassung (RCWL-0516)
    - mod-wsgi - Gateway für Apache Webserver
- JavaScript:
    - react v.19.2 - UI-Library
    - chart.js v.4.5.1 - Library für graphische Darstellung
    - lucide/react v0.563.0 Icon Library

## Umsetzungen der Kern-Features

### Aufbau

![Tux, the Linux mascot](/screenshots/sensorkabel.jpg)

### 1. Erfassung von Sensordaten (BME680 & RCWL-0516)
Die Erfassung der Umweltdaten erfolgt über den BME680-Sensor, dessen Rohwerte (Gaswiderstand) in einen IAQ-Score umgerechnet werden. Parallel wird über den RCWL-0516 Radarsensor die Plausibilität der Messung (Anwesenheit/Bewegung) geprüft. Zur Systemerfassung werden beide Sensoren als Objekte instanziiert.

**BME680 IAQ Berechnung und Sensorerfassung (`GPIO/sensors/bme680.py`):**
```python
import time
import bme680


class BME680Data:
    """Wraps a single BME680 sensor and provides convenience methods.

    The constructor tries the primary I2C address first and falls back to
    the secondary address if the sensor is not found. After construction the
    sensor is configured with sensible oversampling and filter settings.
    """

    def __init__(self):
        # Try primary address first; fallback to secondary on error.
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        self.configure()

    def data_dump(self):
        """Return a dict of all public attributes from the sensor data object.

        Useful for debugging and initial inspection of sensor fields.
        """
        data_dict = {}
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)
            if not name.startswith('_'):
                data_dict[name] = value
        return data_dict

    def set_data(self):
        """Sample the sensor for up to 15 seconds and populate attributes.

        This method prepares the gas measurement heater profile and then
        polls the sensor for up to 15 seconds. When `heat_stable` becomes
        True the IAQ value is computed and the instance is returned. If a
        stable VOC value cannot be established the method raises `IOError`.
        """
        self.prepare_voc_read()
        start = time.perf_counter()
        while time.perf_counter() - start < 15:
            if self.sensor.get_sensor_data():
                self.temperature = round(self.sensor.data.temperature, 2)
                self.pressure = round(self.sensor.data.pressure, 2)
                self.humidity = round(self.sensor.data.humidity, 2)
                if self.sensor.data.heat_stable:
                    # Convert gas resistance to a simple IAQ-like score.
                    self.voc = self.resistance_to_iaq()
                    return self
        # If no stable VOC reading after the timeout, indicate failure.
        raise IOError

    def resistance_to_iaq(self):
        """Convert raw gas resistance (Ohm) to a 0–500 IAQ-like score.

        The conversion clamps the gas resistance into a fixed range and maps
        that range linearly into 0..500 where higher scores indicate worse
        air quality. The mapping and clamping are project-specific heuristics.
        """
        if self.sensor.data.gas_resistance <= 0:
            return 500

        GAS_MIN = 5000     # very poor air quality
        GAS_MAX = 50000    # very good air quality

        # Clamp gas resistance into the expected interval.
        gas = max(min(self.sensor.data.gas_resistance, GAS_MAX), GAS_MIN)

        # Map clamped resistance into an IAQ-style score (0 best — 500 worst).
        iaq = 500 - ((gas - GAS_MIN) / (GAS_MAX - GAS_MIN) * 500)

        return round(iaq, 1)


    def to_dict(self):
        """Return the last-read measurement attributes as a plain dict.

        The shape matches what the rest of the application expects for
        storing or serializing sensor readings.
        """
        return {
            "temperature": self.temperature,
            "pressure": self.pressure,
            "voc": self.voc,
            "humidity": self.humidity
        }

    def configure(self):
        """Configure oversampling and filter settings for stable readings."""
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

    def prepare_voc_read(self):
        """Enable gas measurement and set heater profile for VOC sampling."""
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)
```

**RCWL Bewegungserkennung (`GPIO/sensors/rcwl.py`):**
```python
class RCWL:
    """Wrapper for the RCWL motion sensor hardware.

    The class attempts to initialise the sensor on GPIO pin 5. If
    initialisation fails the exception is logged — callers should handle
    a missing `self.sensor` attribute if they continue using the instance.
    """

    def __init__(self):
        try:
            self.sensor = MotionSensor(5)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Radar sensor initialization failed")


    def detect_motion(self, duration_s=10):
        """Wait up to `duration_s` seconds for motion and return a boolean.

        This convenience method uses `wait_for_active` under the hood which
        blocks until the sensor becomes active or the timeout elapses.
        It returns `True` if motion was detected within the timeout,
        otherwise `False`.
        """
        motion_detected = self.sensor.wait_for_active(timeout=duration_s)

        return bool(motion_detected)

    @staticmethod
    def check_sensor():
        """Interactive monitoring loop that prints activation events.

        Intended for manual debugging from a terminal: it attaches simple
        print callbacks to activation/deactivation events and then blocks on
        `pause()` until interrupted with Ctrl+C.
        """
        sensor = MotionSensor(5)
        try:
            while True:
                # Attach human-readable callbacks that include a timestamp.
                sensor.when_activated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Bewegung erkannt!")
                sensor.when_deactivated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Bewegung mehr.")
                print("Warte auf Bewegung...")
                pause()
        except KeyboardInterrupt:
            print("Beende Monitoring...")
            pass

```

### 2. Automatisierte Datenpflege
Ein Django Management Command steuert das regelmäßige Auslesen und die persistente Speicherung der Daten. Zudem werden alte Datenstände entsprechend den Anforderungen automatisiert bereinigt. Alle dabei auftretenden Ereignisse werden in 'app.log' festgehalten. Bei Fehlern wie Abbrüchen der Datenbankverbindung oder der Sensorik generiert der Django-Logger neue Einträge über die Art der Fehler. 

**Datenbereinigung (`GPIO/models.py`):**
```python
def cleanup_entries(cls, timespan=30):
    # Entfernt Einträge, die älter als 30 Tage sind
    cutoff = timezone.now() - timezone.timedelta(days=timespan)
    result = cls.objects.filter(timestamp__lt=cutoff)
    deleted, _ = result.delete()
    return deleted
```

**Messvorgang (`GPIO/management/commands/measure.py`):**
```python
from GPIO.models import SensorValues
from GPIO.sensors.bme680 import BME680Data
from GPIO.sensors.rcwl import RCWL
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    # Short description shown in `manage.py help`.
    help = "Adds a sensor measurements to the database"

    def get_sensor_read(self):
        """Read the BME680 sensor and return a plain dict of values.

        This method constructs a `BME680Data` instance, triggers a short
        sampling sequence via `set_data()` and converts the result to a
        dictionary with `to_dict()` so it can be persisted.
        """
        handler = BME680Data()
        return handler.set_data().to_dict()

    def is_plausible(self):
        """Return a boolean indicating if the read is plausible.

        Uses the RCWL radar sensor to detect presence/motion. If motion is
        detected the reading is considered plausible. The method returns
        `True`/`False` accordingly.
        """
        radar_sensor = RCWL()
        return radar_sensor.detect_motion()

    def handle(self, *args, **options):
        """Main command entry point: read sensors and save to DB.

        The method logs a summary on success and logs the exception on any
        failure during reading or saving. Persistence is delegated to
        `SensorValues.save_values` (model-layer helper).
        """
        logger = logging.getLogger(__name__)
        try:
            data = self.get_sensor_read()
            data["is_plausible"] = self.is_plausible()
            data["timestamp"] = timezone.now()
            # Persist data using the model helper; keep persistence logic
            # in the model to maintain single responsibility.
            SensorValues.save_values(**data)
            logger.info("New data: {0} C, {1} hPa, {2} rH[%], {3} [IAQ]".format(
                data["temperature"],
                data["pressure"],
                data["humidity"],
                data["voc"]
            ))
        except Exception as error:
            # Log any exception during read/save so the scheduler can inspect
            # the log for problems.
            logger.error(f"{error} database operation failed")
```

### 3. Weboberfläche (React Dashboard)
Das Frontend basiert auf React und ruft die aktuellen Messwerte über eine API ab, um sie visualisiert darzustellen.

**Datenabruf im Dashboard (`frontend/components/Dashboard.jsx`):**
```javascript
const fetchLatest = async (endpoint) => {
    try {
        const response = await fetch(endpoint);
        const result = await response.json();
        setLatest(result);
    } catch (error) {
        console.error(error.message);
        setLatest([]);
    }
};
```
### 4. Datenbank-Schnittstelle

Die Models aus der Django-Applikation können genutzt werden um einfach Endpunkte für den Datenabruf im Frontend abzubilden.

**Abrufbare-Urls (`GPIO/urls.py`):**
Im Django-Controller lassen sich sehr einfach Endpunkte deklarieren. Die Geschäftslogik ist dabei in den GPIO-models gekapselt.

```python
urlpatterns = [
    path("", views.index, name="home"),
    path("api/temps", views.fetch_temperatures, name="temps"),
    path("api/humids", views.fetch_humidities, name="humids"),
    path("api/vocs", views.fetch_vocs, name="vocs"),
    path("api/all", views.fetch_latest, name="latest"),
    path("api/regression", views.fetch_training_data, name="regression"),
    path("logs", views.fetch_log, name="log"),
    path('predict/guests/', views.predict_persons),
]
```

### 5. Regressionsanalyse
Auf Basis der gesammelten Daten wird eine Regressionsanalyse durchgeführt, um Vorhersagen (z.B. Temperaturentwicklung basierend auf Gästeanzahl) zu treffen.

**Vorhersage-Logik (`frontend/utils/prediction.js`):**
```javascript
class PredictionHelper {
    constructor(slope, intercept) {
        this.slope = slope;
        this.intercept = intercept;
    }

    predict(x) {
        // Lineare Regression: y = m * x + b
        return this.slope * x + this.intercept;
    }
    /**
     * 
     * @param data array of person count from the regression data
     * @returns an array of corresponding xy-pairs to visualize the regression line  
     */
    getXYValues(data) {
        return data.map(x => [parseFloat(x), this.predict(x)])
    }
}
```

**UI-Integration der Vorhersage (`frontend/components/Prediction.jsx`):**
```javascript
const yValue = useMemo(() => {
    if (xValue === "") return "";
    let result = Math.round(slope * parseInt(xValue, 10) + intercept);
    if (result > 36) result = "36 (Maximalwert)"
    return result 
}, [xValue, slope, intercept]);
```

## Anleitungen