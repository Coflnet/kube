from django.contrib import admin
from .models import Spieler, Saison, Mannschaft, Spielwoche, Spiel
# Register your models here.

admin.site.register(Spieler)
admin.site.register(Saison)
admin.site.register(Mannschaft)
admin.site.register(Spielwoche)
admin.site.register(Spiel)