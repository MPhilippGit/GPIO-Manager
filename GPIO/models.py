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

      result = cls.objects.filter(timestamp__lt=cutoff)
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


class SensorCSVExporter:
   HEADERS = ["timestamp", "temperature", "voc_value"]

   @staticmethod
   def row(sensor_data: SensorValues):
      timestamp, temperature, voc_value = SensorCSVExporter.HEADERS
      return {
         timestamp: sensor_data.timestamp,
         temperature: sensor_data.temperature,
         voc_value: sensor_data.voc
      }
