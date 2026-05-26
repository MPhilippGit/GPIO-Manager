#!/usr/bin/python3
import argparse
import json
import sys
import time

import bme680


def configure(sensor):
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)


def prepare_voc_read(sensor):
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)


def resistance_to_iaq(sensor):
    if sensor.data.gas_resistance <= 0:
        return 500
    GAS_MIN = 5000
    GAS_MAX = 50000
    gas = max(min(sensor.data.gas_resistance, GAS_MAX), GAS_MIN)
    return round(500 - ((gas - GAS_MIN) / (GAS_MAX - GAS_MIN) * 500), 1)


def read_once(sensor):
    prepare_voc_read(sensor)
    start = time.perf_counter()
    while time.perf_counter() - start < 15:
        if sensor.get_sensor_data():
            temperature = round(sensor.data.temperature, 2)
            pressure = round(sensor.data.pressure, 2)
            humidity = round(sensor.data.humidity, 2)
            if sensor.data.heat_stable:
                return {
                    "temperature": temperature,
                    "pressure": pressure,
                    "humidity": humidity,
                    "voc": resistance_to_iaq(sensor),
                }
    raise IOError("Stable VOC reading not achieved within timeout")


def monitor(sensor):
    prepare_voc_read(sensor)
    print("Open reading stream")
    try:
        while True:
            if sensor.get_sensor_data():
                output = f"{sensor.data.temperature} C,{sensor.data.pressure} hPa,{sensor.data.humidity} %RH"
                if sensor.data.heat_stable:
                    output += f", {sensor.data.gas_resistance}"
                else:
                    print("Heat unstable...")
                print(output)
            else:
                print("Preparing data...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Beende Monitoring...")


def main():
    parser = argparse.ArgumentParser(description="Read BME680 sensor")
    parser.add_argument("--monitor", action="store_true", help="Run interactive monitoring loop")
    args = parser.parse_args()

    try:
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        configure(sensor)
    except Exception as e:
        print(f"Sensor init failed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.monitor:
        monitor(sensor)
    else:
        try:
            data = read_once(sensor)
            print(json.dumps(data))
        except IOError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
