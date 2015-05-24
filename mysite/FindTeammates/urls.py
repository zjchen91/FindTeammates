from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',

    url(r'^roster/$', views.roster),
    url(r'^roster/(?P<courseID>[0-9]+)/$', views.roster_with_courseID),
    url(r'^teams/(?P<courseID>[0-9]+)/$', views.teams),
	url(r'^site/$', views.site, name='site'),
    url(r'^login/$', views.site_login, name='login'),
    url(r'^callback/$', views.callback),
    url(r'^inviteHis$', views.updateInviteHistory),
    url(r'^joinHis$', views.updateJoinHistory),
    url(r'^accept_join$', views.accept_join),
    url(r'^openteam$', views.openTeam),
    url(r'^addNewTeam$', views.addNewTeam),
    url(r'^site/createCourse$', views.createCourse),
    url(r'^registerCourse$', views.registerCourse),
    url(r'^showMessages$', views.showMessages, name="showMessages"),
    url(r'^myTeams$', views.myTeams, name="myTeams"),
    url(r'^team_detail/(?P<teamID>[0-9]+)/$', views.team_detail),


)