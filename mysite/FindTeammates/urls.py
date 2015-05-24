from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    
    url(r'^roster$', views.roster, name='roster'),
    url(r'^teams/$', views.teams, name='teams'),
	url(r'^site/$', views.site, name='site'),
    url(r'^login/$', views.site_login, name='login'),
    url(r'^callback/$', views.callback),
    url(r'^inviteHis$', views.updateInviteHistory),
    url(r'^joinHis$', views.updateJoinHistory),
    url(r'^openteam$', views.openTeam),
    url(r'^addNewTeam$', views.addNewTeam),
    url(r'^createCourse$', views.createCourse),
    url(r'^registerCourse$', views.registerCourse),
    url(r'^showMessages$', views.showMessages, name="showMessages"),
    url(r'^team_detail/(?P<teamID>[0-9]+)/$', views.team_detail),

)