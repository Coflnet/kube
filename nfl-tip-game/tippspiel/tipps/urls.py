
from django.urls import path

from . import views

urlpatterns = [
  path('', views.tipp, name='index'),
  #path('tipp/', views.tipp, name='tipp'),
  path('<woche>', views.index, name='index'),
]
