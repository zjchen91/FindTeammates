from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^roster/$', views.roster, name='roster'),
    url(r'^teams/$', views.teams, name='teams'),

    url(r'^login/$', views.login, name='login'),

    url(r'^inviteHis$', views.updateInviteHistory),
    url(r'^joinHis$', views.updateJoinHistory),
    url(r'^openteam$', views.openTeam),
    url(r'^addNewTeam$', views.addNewTeam),

]