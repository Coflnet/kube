import datetime
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from . import scrape
from django import forms
import tabelle.models
from .scrape import Season
from tabelle.models import Saison, Spielwoche, Spiel, Mannschaft
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
import config


def your_script(url="https://www.nfl.com/schedules/2021/REG1/"):
    games_list = scrape.scrape_wochen_daten(url)
    return games_list


@login_required
def anlegen(request):
    response = "Du siehst den Spieltag und die Tabelle %s)"
    template = loader.get_template('tabelle/index2.html')
    context = {'response': response, 'media': config.media_url}
    return HttpResponse(template.render(context, request))


def long_game_names(season):
    mannschaften = Mannschaft.objects.all()
    for w in season.weeks:
        for s in w.games:
            for m in mannschaften:
                if s.mannschaft_1 in m.name:
                    s.mannschaft_1 = m.name
                    s.bild_1 = m.logo
                    print(s.mannschaft_1 + ' in ' + m.name)
                if s.mannschaft_2 in m.name:
                    s.mannschaft_2 = m.name
                    s.bild_2 = m.logo
                    print(s.mannschaft_2 + ' in ' + m.name)
    return season


@permission_required('add_spiel')
def index(request):
    template = loader.get_template('tabelle/anlegen.html')
    season = scrape.scrape_all()
    season = long_game_names(season)
    scrape.save_season_to_db(season)

    context = {'saison': season, 'media': config.media_url}
    return HttpResponse(template.render(context, request))


@permission_required('add_spiel')
def anlegen_woche(request, woche):
    response = "Du siehst den Spieltag und die Tabelle %s)"
    template = loader.get_template('tabelle/anlegen.html')
    # games = your_script()
    context = {'response': response, 'saison': woche, 'media': config.media_url}
    return HttpResponse(template.render(context, request))
