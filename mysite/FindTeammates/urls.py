from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^roster/$', views.roster, name='roster'),
    url(r'^teams/$', views.teams, name='teams'),
    url(r'^ajax$', views.ajax, name='ajax'),
    url(r'^test$', views.main),
    url(r'^inviteHis$', views.updateInviteHistory),
]