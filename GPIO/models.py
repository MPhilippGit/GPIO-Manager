"""Database models and small helpers for sensor data.

This module defines the `SensorValues` model which stores readings from
the BME680 sensor and a tiny helper `SensorCSVExporter` used when
exporting training CSVs. The module contains a few convenience methods
that keep calling code (management commands, views) compact.
"""

from django.db import models
from django.utils import timezone
import logging


class SensorValues(models.Model):
   """Model representing a single sensor measurement.

   Fields mirror the physical sensor output and include a boolean
   `is_plausible` which higher-level logic uses to filter unreliable
   readings (e.g. when no presence was detected by the radar sensor).
   """

   voc =  models.DecimalField(max_digits=10, decimal_places=2, db_column="voc")
   pressure =  models.DecimalField(max_digits=10, decimal_places=2, db_column="pressure")
   timestamp = models.DateTimeField(db_column="timestamp")
   temperature =  models.DecimalField(max_digits=10, decimal_places=2, db_column="temperature")
   humidity =  models.DecimalField(max_digits=10, decimal_places=2, db_column="humidity")
   is_plausible = models.BooleanField(db_column="is_plausible")

   def cleanup_entries(cls, timespan=30):
      """Delete rows older than `timespan` days and return deleted count.

      The method computes a cutoff datetime and removes any rows with a
      `timestamp` earlier than the cutoff. It returns the number of rows
      deleted so callers (management commands) can log the result.
      """
      cutoff = timezone.now() - timezone.timedelta(days=timespan)

      result = cls.objects.filter(timestamp__lt=cutoff)
      deleted, _ = result.delete()
      return deleted

   @staticmethod
   def save_values(**data):
      """Create and persist a `SensorValues` instance from a values dict.

      This helper centralises the field mapping used by management commands
      and keeps their code concise. The function expects the dict to
      contain keys matching the model field names.
      """
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
   """Small helper to produce CSV rows for training/export.

   `HEADERS` defines the CSV columns used elsewhere in the project. The
   `row` static method accepts a `SensorValues` instance and returns a
   dict matching `HEADERS` so it can be written using `csv.DictWriter`.
   """

   HEADERS = ["timestamp", "temperature", "voc_value"]

   @staticmethod
   def row(sensor_data: SensorValues):
      # Unpack header names for clarity and return a mapping used by CSV
      # writers throughout the codebase.
      timestamp, temperature, voc_value = SensorCSVExporter.HEADERS
      return {
         timestamp: sensor_data.timestamp,
         temperature: sensor_data.temperature,
         voc_value: sensor_data.voc
      }
