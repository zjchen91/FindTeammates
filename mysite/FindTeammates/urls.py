from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.roster, name='roster'),
    url(r'^roster/$', views.roster, name='roster'),
    url(r'^teams/$', views.teams, name='teams'),
]