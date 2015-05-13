from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from linkedin import linkedin
import urllib2

'''
<<<<<<< HEAD
API_KEY = '773xw0mljix91p'
API_SECRET = 'ktG99eRUuMnZ80eW'
USERNAME = "phoebe996@gmail.com"
PASSWORD = "njdx3119wyw"
TOP_URL = "http://www.linkedin.com"

def roster(request):

	return render_to_response('FindTeammates/roster.html')
=======
'''
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import socket
from FindTeammates.models import *





def roster(request):
	return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))


def teams(request):
	stpair = student_team.objects.all()
	if len(stpair.filter(studentID=current_id)) != 0:
		return render_to_response('FindTeammates/teams.html')
	else:
		'''
		DO recommander
		'''
		return render_to_response('FindTeammates/teams.html')
	
def login(request):
	
	RETURN_URL = 'http://localhost:8000/FindTeammates/'

	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values()[:1])
	print linkedin.PERMISSIONS.enums.values()[0]
	print authentication.authorization_url  # open this url on your browser
	#application = linkedin.LinkedInApplication(authentication)
	#http://localhost:8000/FindTeammates/?code=AQR5MryHH-PrPjBguVK8suK-4s8FSBip5KIYxTPl0ps1RZY1tsYScut4KsWblKU0vibFLRBav5jlp9d2SNj1PSWUBPX_gX6ZmuYIPzlMwS4RDK6ygzY&state=360a3fc85fede5771d61480973a46f4a
	#http://localhost:8000/FindTeammates/?code=AQQupO6iTYMJrFuFH3P-EJTsIo9cN6nDi8yj0PArsll41n9WQfVmBQo8y-Hrz2SyMkfAC6mLjNLQG0V__VwZr4npC1sFTlAIku3BtT-KaEP5w9MlRzM&state=0a19199cf14173394df29fc2e682299f
	#http://localhost:8000/FindTeammates/?code=AQTR9xUM7SuPw5xs4OVTrhjARrXWVPET5WrG3fQaDAgZsB_9HZgdFD_YFOIrn-T2vFs5i9MFGl1ZpbeVeokEyCue2wiEQH1iPILJbSYTqtZx86HUBH4&state=7873719d9118e017c81e7b9df825a6ad
	code='AQSZCB99ep3gA9hXl9s6aNoT-_dCiO5VzybF17zYiwU3ZvRp7c5Km0ErtyuY3FuYWvalrSHr9rpuUmvKUvfF0evof6FpMAg33Wv0ehKljJJuHZBq9r4'
	authentication.authorization_code = code
	#token=authentication.get_access_token()
	#application = linkedin.LinkedInApplication(token=token)
	#url = application.get_profile()
	url ="https://www.linkedin.com/profile/view?id=334119363&trk=hp-identity-photo"
	print url

	# create a password manager
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

	# Add the username and password.
	# If we knew the realm, we could use it instead of None.
	password_mgr.add_password(None, url, USERNAME, PASSWORD)

	handler = urllib2.HTTPBasicAuthHandler(password_mgr)

	# create "opener" (OpenerDirector instance)
	opener = urllib2.build_opener(handler)

	# use the opener to fetch a URL
	opener.open(url)

	# Install the opener.
	# Now all calls to urllib2.urlopen use our opener.
	urllib2.install_opener(opener)
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	print "----------------"
	source_code = str(resp.read().decode())
	print source_code
	'''
	i = source_code.find("skill")
	while i>0:
		print "yay"
		i = i+17
		skill = ""
		while(not source_code[i]=='"'):
			skill = skill + source_code[i]
			i=i+1
		print skill
		i = source_code.find("fmt__skill_name")
	'''
	return render_to_response("FindTeammates/login.html")



def updateInviteHistory(request):

	if request.POST.has_key('client_response'):
		print 'shit'
		x = request.POST['client_response']
		'''
		TODO:
		update invite history in database
		'''
		print x
		
		return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))
	else:
		return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))

def updateJoinHistory(request):

	if request.POST.has_key('client_response'):
		print 'shit'
		x = request.POST['client_response']
		'''
		TODO:
		update join history in database
		'''
		print x
		
		return render_to_response('FindTeammates/teams.html', context_instance=RequestContext(request))
	else:
		return render_to_response('FindTeammates/teams.html', context_instance=RequestContext(request))

def openTeam(request):
	return render_to_response('FindTeammates/openTeam.html', context_instance=RequestContext(request))


def addNewTeam(request):
	current_id = '1'
	current_course_id = '1'
	team_name = request.POST.get("teamName", "")
	description = request.POST.get("teamDescription", "")
	teamSize = request.POST.get("teamSize", "")
	print team_name
	print description
	print teamSize
	team = Team(teamName=team_name, teamDescription=description, Size=teamSize, ownerID=current_id, \
		courseID=current_course_id)
	team.save()
	stu_team = student_team(studentID=current_id, teamID=team.id)
	stu_team.save()
	return render_to_response('FindTeammates/teams.html')





