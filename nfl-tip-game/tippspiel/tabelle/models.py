from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import (
    DateRangeField,
    RangeBoundary,
    RangeOperators,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime


# User = get_user_model()
# Create your models here.
class Spieler(models.Model):
    name = models.CharField(max_length=50)
    # punkt=models.IntegerField()


class Saison(models.Model):
    dStart = models.DateField()
    dEnde = models.DateField()


class Mannschaft(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(default=None, blank=True, null=True, upload_to='logos/')


# name = models.ForeignKey()
class Spielwoche(models.Model):
    name = models.CharField(max_length=16)
    start = models.DateField()
    ende = models.DateField(default=None, blank=True, null=True)
    saison_fk = models.ForeignKey(Saison, on_delete=models.CASCADE)


class Spiel(models.Model):
    mannschaft1_fk = models.ForeignKey(Mannschaft, on_delete=models.CASCADE, related_name="erste_mannschaft")
    mannschaft2_fk = models.ForeignKey(Mannschaft, on_delete=models.CASCADE, related_name="zweite_mannschaft")
    mannschaft1_punkte = models.IntegerField(default=None, blank=True, null=True)
    mannschaft2_punkte = models.IntegerField(default=None, blank=True, null=True)
    spielwoche_fk = models.ForeignKey(Spielwoche, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mannschaft1_fk) + " gegen " + str(self.mannschaft2_fk)
