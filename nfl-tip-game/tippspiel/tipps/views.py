# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from tabelle.models import Saison, Spielwoche, Spiel, Mannschaft
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from tipps.models import Tipp
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required, permission_required
import config


# from .models import tipp


@login_required
def tipp(request):
    template = loader.get_template('tipps/index.html')
    spielwoche = Spielwoche.objects.filter(saison_fk=Saison.objects.filter().order_by('-id')[0],
                                           start__gt=datetime.datetime.now()).order_by('start')
    spiele = Spiel.objects.filter(spielwoche_fk=spielwoche[0])


    tipps = Tipp.objects.filter(fk_spieler_id_neu = request.user.id, fk_spiel=spiele[0])
    if tipps:
        template = loader.get_template('tipps/tipps_anzeigen.html')
        context = {'tipps': tipps, 'spielwoche': spielwoche}
        return HttpResponse(template.render(context, request))
    if request.method == 'POST':
        save_tipps(request, spiele)
        return HttpResponse("Getippt")
    context = {'spiele': spiele, 'spielwoche': spielwoche, 'media': config.media_url}
    return HttpResponse(template.render(context, request))



def save_tipps(request, spiele):
    for spiel in spiele:
        choice = request.POST.get(str(spiel.id))
        print(choice)
        t, b = Tipp.objects.get_or_create(fk_spieler_id_neu=request.user,
                                          fk_spiel=spiel,
                                          defaults={'itipp': choice})
        t.itipp = choice
        t.save()

@login_required
def index(request, woche):
    template = loader.get_template('tipps/index.html')
    print(woche)
    try:
        woche = int(woche)
    except:
        return HttpResponse("Zahl eingeben")
    spielwoche = Spielwoche.objects.filter(saison_fk=Saison.objects.filter().order_by('-id')[0])
    if woche>len(spielwoche)+1:
        return HttpResponse("Das gibts doch gar nicht")
    spiele = Spiel.objects.filter(spielwoche_fk=spielwoche[woche-1])
    tipps = []
    for spiel in spiele:
        tipp = Tipp.objects.filter(fk_spieler_id_neu=request.user.id, fk_spiel=spiel)
        if tipp:
            tipps.append(tipp[0])
    if tipps:
        template = loader.get_template('tipps/tipps_anzeigen.html')
        context = {'tipps': tipps, 'spielwoche': spielwoche, 'media': config.media_url}
        return HttpResponse(template.render(context, request))
    if request.method == 'POST':
        save_tipps(request, spiele)
        return HttpResponseRedirect(request.get_full_path())
    context = {'spiele': spiele, 'spielwoche': spielwoche, 'media': config.media_url}
    return HttpResponse(template.render(context, request))
