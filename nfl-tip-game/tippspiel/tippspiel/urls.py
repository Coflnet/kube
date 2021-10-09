"""tippspiel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('tipps/', include('tipps.urls')),
    path('tabelle/', include('tabelle.urls')),
    path('scrape/', include('scrape.urls')),
    # path('admin/', admin.site.urls, name=admin),
    path('', admin.site.urls, name=admin),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
