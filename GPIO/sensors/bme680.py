"""Helpers for reading and converting data from a BME680 sensor.

This module wraps the `bme680` library with a small class that handles
initialisation, configuration and a few convenience methods used by the
application:

- `BME680Data.set_data()` performs a short sampling period and returns the
  object with `temperature`, `pressure`, `humidity` and `voc` attributes set.
- `resistance_to_iaq()` converts the raw gas resistance value to a simple
  IAQ-like 0–500 score used by the project UI.
"""

import logging
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

    def check_sensor(self):
        """Interactive monitoring loop that prints sensor output to stdout.

        Intended for manual debugging from the command line. It repeatedly
        polls the sensor and prints a human-readable summary. The loop can
        be stopped with Ctrl+C (KeyboardInterrupt).
        """
        print("Open reading stream")
        self.prepare_voc_read()
        print(f"Initial read: {self.data_dump()}")
        try:
            while True:
                if self.sensor.get_sensor_data():
                    output = f"{self.sensor.data.temperature} C,{self.sensor.data.pressure} hPa,{self.sensor.data.humidity} %RH"
                    if self.sensor.data.heat_stable:
                        output = output + f", {self.sensor.data.gas_resistance}"
                    else:
                        print("Heat unstable...")
                    print(output)
                else:
                    print("Preparing data...")
                time.sleep(5)

        except KeyboardInterrupt:
            print("Beende Monitoring...")

