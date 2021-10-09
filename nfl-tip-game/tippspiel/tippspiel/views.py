from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from ..tabelle.models import Tipp
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'tabelle/index.html'
    context_object_name = 'Startseite'


class DetailView(generic.DetailView):
    model = Tipp
    template_name = 'tipps/index.html'


class ResultsView(generic.DetailView):
    model = Tipp
    template_name = 'tabelle/result.html'

# def vote(request, spiel_id):
#   getippt = get_object_or_404(Tipp, pk= spiel_id)
# try:
# manschaft1 = tipps
