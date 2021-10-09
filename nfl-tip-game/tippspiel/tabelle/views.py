from django.contrib.auth.models import User
from django.shortcuts import render
import config
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Saison, Spielwoche, Spiel, Mannschaft
from tipps.models import Tipp
from django.contrib.auth.decorators import login_required, permission_required


class AuswertungSpieler:
    def __init__(self, spieler, auswertungen, punkte):
        self.spieler = spieler
        self.auswertungen = auswertungen
        self.punkte = punkte

    def get_punkte(self):
        return self.punkte


class Auswertung:
    def __init__(self, spiel, tipp):
        self.spiel = spiel
        self.tipp = tipp
        self.punkte = 0


    def auswerten(self, user, t):
        if self.spiel.mannschaft1_punkte > self.spiel.mannschaft2_punkte:
            winner = 1
        else:
            winner = 2
        if winner != self.tipp.itipp:
            return 0
        tipps = Tipp.objects.filter(fk_spiel=self.spiel, ).exclude(fk_spieler_id_neu_id=user)
        if len(tipps) == 0:
            return 5
        for i in tipps:
            if t.itipp == self.tipp.itipp:
                return 3
        return 5


def auswerten_spieler(user, spiele):
    spiele_tipps = []
    for s in spiele:
        try:
            t = Tipp.objects.get(fk_spiel=s, fk_spieler_id_neu_id=user)
            spiele_tipps.append(Auswertung(s, t))
        except:
            pass
    punkte = 0
    for st in spiele_tipps:
        st.punkte = st.auswerten(user, t)
        if st.punkte == 5 or st.punkte == 3:
            st.tipp_richtig = 'green'
            if st.tipp.itipp == 1:
                st.mannschaft1_color = 'green_font'
                st.mannschaft2_color = 'red_font'
            else:
                st.mannschaft1_color = 'red_font'
                st.mannschaft2_color = 'green_font'
        else:
            if st.tipp.itipp == 2:
                st.mannschaft1_color = 'green_font'
                st.mannschaft2_color = 'red_font'
            else:
                st.mannschaft1_color = 'red_font'
                st.mannschaft2_color = 'green_font'
            st.tipp_richtig = 'red'
        if st.tipp.itipp == 1:
            st.tipp_m1 = 'green'
            st.tipp_m2 = 'gray'
        else:
            st.tipp_m1 = 'gray'
            st.tipp_m2 = 'green'

        punkte += st.punkte
    return spiele_tipps, punkte



@login_required
def index(request):
    template = loader.get_template('tabelle/auswertung.html')
    saison = Saison.objects.all().order_by("-id")[0]
    spielwochen = Spielwoche.objects.filter(saison_fk=saison)
    spiele = []
    for w in spielwochen:
        spiele += Spiel.objects.filter(spielwoche_fk=w).exclude(mannschaft1_punkte=None, mannschaft2_punkte=None)
    a = auswerten_spieler(request.user, spiele)
    ausw = [AuswertungSpieler(request.user, a[0], a[1])]
    context = {'auswertungen_spieler': ausw, 'media': config.media_url}
    return HttpResponse(template.render(context, request))


@login_required
def results(request):  # , spieltag):
    template = loader.get_template('tabelle/auswertung.html')
    saison = Saison.objects.all().order_by("-id")[0]
    spielwochen = Spielwoche.objects.filter(saison_fk=saison)
    spiele = []
    for w in spielwochen:
        spiele += Spiel.objects.filter(spielwoche_fk=w).exclude(mannschaft1_punkte=None, mannschaft2_punkte=None)
    user = User.objects.filter()
    ausw = []
    up = []
    for u in user:
        a = auswerten_spieler(u, spiele)
        buff =AuswertungSpieler(u, a[0], a[1])
        ausw.append(buff)
        ausw.sort(key=lambda b: b.punkte)

    ausw.reverse()
    #for spiel in ausw:
     # sort_ausw = ausw.sort(spiel.punkte)
    #aus = []
    #for i in range(len(ausw)):
     #   max = 0
      #  index = 0
       # j = 0
        #for a in ausw:
        #    if a.punkte > max:
         #       max = a.punkte
          #      index = j
           # j+= 1
        #print(max)
        #aus.append(ausw[index])
        #ausw.remove(ausw[index])




    context = {'auswertungen_spieler': ausw, 'media': config.media_url}
    return HttpResponse(template.render(context, request))

@login_required
def auswertung(request):
    if request.user.is_authenticated:
        username = request.user.username
    # hier kommt die Auswertung der Spielergebnisse eines Spielers hin
    saison = Saison.objects.all().order_by("-id")[0]
    spielwochen = Spielwoche.objects.filter(saison_fk=saison)
    spiele = []
    for w in spielwochen:
        spiele += Spiel.objects.filter(spielwoche_fk=w)
    tipps = []
    for s in spiele:
        tipps += Tipp.objects.filter(fk_spiel=s, fk_spieler_id=request.user.id)
    tipps_ausgewertet = []
    for t in tipps:
        pass
    template = loader.get_template('tabelle/auswertung.html')
    context = {'username': username, 'media': config.media_url}
    return HttpResponse(template.render(context, request))