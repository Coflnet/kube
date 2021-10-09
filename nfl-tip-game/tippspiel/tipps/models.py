# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from tabelle.models import Spiel, Spieler
from django.core.exceptions import ValidationError


def validate_tipp(tipp):
    if tipp != 1 and tipp != 2:
        raise ValidationError('%(tipp)s ist nicht 1 oder 2',
                              params={'tipp': tipp},
                              )

class Tipp(models.Model):
    itipp = models.IntegerField(validators=[validate_tipp])
    fk_spieler_id_neu = models.ForeignKey(User, on_delete=models.CASCADE)
    #fk_spieler_id = models.ForeignKey(Spieler, on_delete=models.CASCADE)
    fk_spiel = models.ForeignKey(Spiel, on_delete=models.CASCADE)



