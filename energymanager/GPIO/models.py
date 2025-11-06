from django.db import models

# Create your models here.

class TemperatureValue(models.Model):
   measurement = models.CharField(max_length=255)
   date = models.DateTimeField("timestamp")

class RadarSensoreValue(models.Model):
   measurement = models.CharField(max_length=255)
   date = models.DateTimeField("timestamp")