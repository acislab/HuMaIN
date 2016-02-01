"""humain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'main.views.index', name='index'),
    url(r'^mission.html', 'main.views.mission', name='mission'),  
    url(r'^app.html', 'main.views.app', name='app'),
    url(r'^catalog.html', 'main.views.catalog', name='catalog'),
    url(r'^contact.html', 'main.views.contact', name='contact'),
    url(r'^help.html', 'main.views.help1', name='help'),
    url(r'^cropLabel.html', 'main.views.cropLabelView', name='cropLabelView'),
    url(r'^cropFields.html', 'main.views.cropFieldsView', name='cropFieldsView'),
    url(r'^admin/', include(admin.site.urls)),
]
