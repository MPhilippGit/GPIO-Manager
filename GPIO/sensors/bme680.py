import logging
import time
import bme680

class BME680Data:
    def __init__(self):
        # initialize
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        self.configure()

    def data_dump(self):
        """returns a dictionary for every possible measurement from the sensor"""
        data_dict = {}
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)
            if not name.startswith('_'):
                data_dict[name] = value
        return data_dict

    def configure(self):
        """Sets sample and filter sizes"""
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

    def prepare_voc_read(self):
        """Enables gas measurement and aims to stabilize """
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

    def get_full_read(self):
        self.prepare_voc_read()
        """Trys to fetch data when heat is stable for gas measurement. Warning log if heat can't be stabilized"""
        i = 0
        while i < 10:
            if not self.sensor.data.heat_stable:
                i+=1
                time.sleep(1)
                continue
            return self.data_dump()
        BME680Data.log_unstable_read()
        return self.data_dump()

    @staticmethod
    def log_unstable_read():
        logger = logging.getLogger(__name__)
        logger.warning("No stable VOC read")



# sampling settings

# for name in dir(sensor.data):
#     value = getattr(sensor.data, name)

#     if not name.startswith('_'):
#         print('{}: {}'.format(name, value))



# # Up to 10 heater profiles can be configured, each
# # with their own temperature and duration.
# # sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# # sensor.select_gas_heater_profile(1)
