from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from linkedin import linkedin
import urllib2
from cookie import *
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
from FindTeammates.recommender import *
import re




def roster(request):
	current_id = 17
	current_course_id = 1

	stpair = student_team.objects.all()
	studentObjectList = student_course.objects.all().filter(courseID=current_course_id)
	#studentObjectList = Student.objects.all()
	alluser = []
	for stu in studentObjectList:
		alluser.append(str(stu.studentID.id))
	template = loader.get_template('FindTeammates/roster.html')
	# see whether current user is in a team or not
	# in a team
	if len(stpair.filter(studentID=current_id)) != 0:

		preferuser = {}
		inviteHis = teamInviteStuHistory.objects.all()
		for invite in inviteHis:
			ter = str(invite.inviterID.id)
			tee = str(invite.inviteeID.id)
			if ter in preferuser:
				preferuser[ter].append(tee)
			else:
				preferuser[ter] = [tee]
		test = recommander(str(current_id), 'team', preferuser, alluser)
		ranklist = test.run()
		studentObjectList = []
		for item in ranklist:
			studentObjectList.append(Student.objects.get(id=int(item)))

		context = RequestContext(request, {'student_list': studentObjectList})
		return HttpResponse(template.render(context))
	else:
		context = RequestContext(request, {'student_list': studentObjectList})
		return HttpResponse(template.render(context))


def site(request):
	return render_to_response("FindTeammates/site.html")



def teams(request):
	current_id = 17
	current_course_id = 1
	stpair = student_team.objects.all()
	teamObjectList = Team.objects.all().filter(courseID=current_course_id)
	allteam = []
	for team in teamObjectList:
		allteam.append(str(team.id))
	template = loader.get_template('FindTeammates/teams.html')
	# in a team
	if len(stpair.filter(studentID=current_id)) != 0:
		context = RequestContext(request, {'team_list': teamObjectList})
		return HttpResponse(template.render(context))
	else:
		preferteam = {}
		joinHis = stuJoinTeamHistory.objects.all()
		for join in joinHis:
			ner = str(join.joinerID.id)
			nee = str(join.joineeTeamID.id)
			if ner in preferteam:
				preferteam[ner].append(nee)
			else:
				preferteam[ner] = [nee]
		print preferteam
		test = recommander(str(current_id), 'team', preferteam, allteam)
		ranklist = test.run()
		studentObjectList = []
		for item in ranklist:
			teamObjectList.append(Team.objects.get(id=int(item)))
		context = RequestContext(request, {'team_list': teamObjectList})
		return HttpResponse(template.render(context))

# From Enrui, New listening subAddress
# If I missed something, let me know ASAP.
# Listen to the server call back, 
# the linkedin server redirect browser to this addr with the pass code,
# this code is use to exchange the token
# with this code, we can get the basic_profile and the url
# this url is used for my parser,
# the parser login with an valid linked account and save cookie.
# so it can open any url of full information
'''##example information in basic_profile
{u'headline': u'Student at Columbia University in the City of New York',
u'lastName': u'Liao', 
u'siteStandardProfileRequest': {u'url': u'https://www.linkedin.com/profile/view?id=192228977&authType=name&authToken=nnct&trk=api*a3740053*s3809493*'},
u'id': u'ejEsklXpRl', 
u'firstName': u'Enrui'}
'''

def callback(request):
	code = request.args['code']
	authentication.authorization_code = code
	t = authentication.get_access_token()
	linkin_App = linkedin.LinkedInApplication(token=t)
	# ~~~~~~~~~~~~~~~~~~get token~~~~~~~~~~~~~~~~
	profile = linkin_App.get_profile()
	profile_url = profile['siteStandardProfileRequest']['url']

	# ~~~~~~~~~~~~~~~~~~~~get info from basic_profile~~~~~~~~~~~~
	profile_id = profile['id']
	profile_name = profile['firstName'] + ' ' + profile['lastName']
	profile_headline = profile['headline']
	skills = []					# default skills and pic in case the parse fail
	profile_pic = ''
	##~~~~~~~~~~ here is the code of parser, or you can call it opener~~~~~~~~~~~
	with open('account.txt','r') as f:
		username = f.readline().split('=')[1].strip(' \t"')
		password = f.readline().split('=')[1].strip(' \t"')
	parser = LinkedInParser(username, password)
	res = parser.loadPage(tart)
	## res contains all the full_profile, here I only parse the skills.
	## Give me a list of things need to be parsed
	## ~~~~~~~~~~~here is the code to parse profile_pic~~~~~~~~~~~~~~~
	try:
		m = re.findall('"profile-picture".+jpg\' width', res)[0]
		for i in range(len(m)):
			n = len("img src='")
			if m[i:i+n] == "img src='":
				start = i + n
				break
		for i in range(start,len(m)):
			if m[i] == "'":
				end = i
				break
		profile_pic = m[start:end]
	except:
		print "parse profile_pic fail because this account don't have access to the profile_pic"
	## ~~~~~~~~~~~~~~here is the code of parsing~~~~~~~~~~~~~~~~~~
	## use regular expression
	# in the example file you can see a example res I get from result, it's the html
	# and an regular.py program use re to find all the skills
	# simply run the program you can see
	try:
		skills = re.findall('data-endorsed-item-name="\w+"', res)
		for i in range(len(skills)):
			skills[i] = skills[i].split('=')[1].strip('"')
	except:
		print "error happened in parsing skills"
	## ~~~~~~~~~~here is the code of adding data to the database~~~~~~~~~~
	# I don't know how to add it, this is a dictionary for you.
	post = {'name':profile_name,		#Enrui Liao
			'skill':skills,				#['Matlab','Java']
			'image':profile_pic,		#(str)
			'url':profile_url,			#(str)
			'headline':profile_headline	#(str)
			}

	## ~~~~~~~~~~~~~~~~~~response whatever data~~~~~~~~~~~~~~~~~~~~~~~~~~
	return render_to_response('FindTeammates/roster.html')

# redirect the browser to Linkedin login page
def login(request):
	addr = 'http://localhost:8000/'
	callback_postfix = 'FindTeammates/callback'
	API_KEY = '77ivy1b3bzxmlk'
	API_SECRET = 'yyZCB6IvxBFinBcO'
	RETURN_URL = addr+ callback_postfix

	permi = linkedin.PERMISSIONS.enums.values()[:1]
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, permi)
	url = authentication.authorization_url	
	return redirect(url)



def updateInviteHistory(request):
	current_id = 17
	if request.POST.has_key('client_response'):
		inviteeID = request.POST['client_response']
		inviter = Student.objects.get(id=current_id)
		invitee = Student.objects.get(id=inviteeID)
		his = teamInviteStuHistory(inviterID=inviter, inviteeID=invitee)
		his.save()
		
		return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))
	else:
		return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))

def updateJoinHistory(request):
	current_id = 17
	if request.POST.has_key('client_response'):
		jointeamID = request.POST['client_response']
		print jointeamID
		joiner = Student.objects.get(id=current_id)
		jointeam = Team.objects.get(id=jointeamID)
		his = stuJoinTeamHistory(joinerID=joiner, joineeTeamID=jointeam)
		his.save()
		
		return render_to_response('FindTeammates/teams.html', context_instance=RequestContext(request))
	else:
		return render_to_response('FindTeammates/teams.html', context_instance=RequestContext(request))

def openTeam(request):
	return render_to_response('FindTeammates/openTeam.html', context_instance=RequestContext(request))


def addNewTeam(request):
	current_id = 17
	current_course_id = 1

	team_name = request.POST.get("teamName", "")
	description = request.POST.get("teamDescription", "")
	teamSize = request.POST.get("teamSize", "")
	stu = Student.objects.get(id=current_id)
	course = Course.objects.get(id=current_course_id)

	team = Team(teamName=team_name, teamDescription=description, Size=teamSize, ownerID=stu, courseID=course)
	
	team.save()
	
	stu_team = student_team(studentID=stu, teamID=team)
	stu_team.save()
	return teams(request)
	#return render_to_response('FindTeammates/teams.html')
	





