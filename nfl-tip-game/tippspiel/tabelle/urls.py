from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alle/', views.results, name='alle'),
    path('auswertung/<str:woche>', views.auswertung, name='auswertung'),
]
