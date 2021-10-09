from django.db import models

# Create your models here.
class Anmeldung(models.Model):
  benutzer = models.CharField(max_length=200)
  pwd = models.CharField(max_length=200)
