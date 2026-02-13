from django.db import models
from django.utils import timezone
import logging

# Create your models here.

class SensorValues(models.Model):
   voc =  models.DecimalField(max_digits=10, decimal_places=2, db_column="voc")
   pressure =  models.DecimalField(max_digits=10, decimal_places=2, db_column="pressure")
   timestamp = models.DateTimeField(db_column="timestamp")
   temperature =  models.DecimalField(max_digits=10, decimal_places=2, db_column="temperature")
   humidity =  models.DecimalField(max_digits=10, decimal_places=2, db_column="humidity")
   is_plausible = models.BooleanField(db_column="is_plausible")

   def cleanup_entries(cls, timespan=30):
      cutoff = timezone.now() - timezone.timedelta(days=timespan)
      result = cls.objects.filter(timestamp__gt=cutoff)
      deleted, _ = result.delete()
      return deleted

   @staticmethod
   def save_values(**data):
      entry = SensorValues(
         timestamp=data["timestamp"],
         temperature=data["temperature"],
         humidity=data["humidity"],
         voc=data["voc"],
         pressure=data["pressure"],
         is_plausible=data["is_plausible"]
      )
      entry.save()

class Measurements(models.Model):
   unit = models.CharField(max_length=50, db_column="unit")
   timestamp = models.DateTimeField(db_column="timestamp")
   is_plausible = models.BooleanField(db_column="is_plausible")

   class Meta:
      abstract = True

   @classmethod
   def cleanup_entries(cls, timespan=30):
      cutoff = timezone.now() - timezone.timedelta(days=timespan)
      result = cls.objects.filter(timestamp__gt=cutoff)
      deleted, _ = result.delete()
      return deleted


class Temperatures(Measurements):
   measurement =  models.DecimalField(max_digits=5, decimal_places=2, db_column="measurement")

   @staticmethod
   def save_temp(measurement, plausibility, timestamp):
      logger = logging.getLogger(__name__)
      try:
         new_measurement = Temperatures(measurement=measurement, is_plausible=plausibility, unit="Celsius", timestamp=timezone.now())
         new_measurement.save()
         logger.info(f"new temperature measurement: {measurement}")
      except Exception as error:
         # Log errors 
         logger.error(f"error while trying to write to db: {error}")

class Humidities(Measurements):
   measurement =  models.DecimalField(max_digits=5, decimal_places=2, db_column="measurement")

   @staticmethod
   def save_humidity(measurement, plausibility, timestamp):
      logger = logging.getLogger(__name__)
      try:
         new_measurement = Humidities(measurement=measurement, is_plausible=plausibility, unit="rH", timestamp=timestamp)
         new_measurement.save()
         logger.info(f"new humidity measurement: {measurement}")
      except Exception as error:
         # Log errors 
         logger.error(f"error while trying to write to db: {error}")

class VOCs(Measurements):
   measurement =  models.DecimalField(max_digits=8, decimal_places=2, db_column="measurement")

   @staticmethod
   def save_voc(measurement, plausibility, timestamp):
      logger = logging.getLogger(__name__)
      try:
         new_measurement = VOCs(measurement=measurement, is_plausible=plausibility, unit="Ohm", timestamp=timestamp)
         new_measurement.save()
         logger.info(f"new voc measurement: {measurement}")
      except Exception as error:
         # Log errors 
         logger.error(f"error while trying to write to db: {error}")

class Pressures(Measurements):
   measurement =  models.DecimalField(max_digits=5, decimal_places=2, db_column="measurement")

   @staticmethod
   def save_pressure(measurement, plausibility, timestamp):
      logger = logging.getLogger(__name__)
      try:
         new_measurement = Pressures(measurement=measurement, is_plausible=plausibility, unit="hPa", timestamp=timestamp)
         new_measurement.save()
         logger.info(f"new pressure measurement: {measurement}")
      except Exception as error:
         # Log errors 
         logger.error(f"error while trying to write to db: {error}")
