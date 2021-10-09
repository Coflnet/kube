from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('anlegen/', views.anlegen, name='anlegen'),
    path('anlegen_woche/<str:woche>/', views.anlegen_woche, name='anlegen_woche'),
]
