from django.shortcuts import render
from django.http import HttpResponse
from django.http import *
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from linkedin import linkedin
import urllib2
from FindTeammates.models import *
from FindTeammates.recommender import *
from django.contrib.auth.models import User
import json
import socket
import re
from cookie import *

API_SECRET = 'ktG99eRUuMnZ80eW'
USERNAME = "phoebe996@gmail.com"
PASSWORD = "njdx3119wyw"
TOP_URL = "http://www.linkedin.com"




def roster(request):
	current_id = 17
	current_course_id = 1

	stpair = student_team.objects.all()
	studentObjectList = student_course.objects.all().filter(courseID=current_course_id)

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

		context = RequestContext(request, {'student_list': studentObjectList, 'courselist':courselist})
		return HttpResponse(template.render(context))
	else:
		context = RequestContext(request, {'student_list': studentObjectList, 'courselist':courselist})
		return HttpResponse(template.render(context))


def site(request):
	print "yayayaya"
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
		context = RequestContext(request, {'team_list': teamObjectList,  'courselist':courselist})
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
		context = RequestContext(request, {'team_list': teamObjectList, 'courselist':courselist})
		return HttpResponse(template.render(context))

'''	
def login(request):
	user = User(id=1000000, password="test")
	user.save()
	print "in login view"
	
	RETURN_URL = 'http://localhost:8000/FindTeammates/'

	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values()[:1])
	print linkedin.PERMISSIONS.enums.values()[0]
	print authentication.authorization_url  # open this url on your browser
	#application = linkedin.LinkedInApplication(authentication)
	#http://localhost:8000/FindTeammates/?code=AQR5MryHH-PrPjBguVK8suK-4s8FSBip5KIYxTPl0ps1RZY1tsYScut4KsWblKU0vibFLRBav5jlp9d2SNj1PSWUBPX_gX6ZmuYIPzlMwS4RDK6ygzY&state=360a3fc85fede5771d61480973a46f4a
	#http://localhost:8000/FindTeammates/?code=AQQupO6iTYMJrFuFH3P-EJTsIo9cN6nDi8yj0PArsll41n9WQfVmBQo8y-Hrz2SyMkfAC6mLjNLQG0V__VwZr4npC1sFTlAIku3BtT-KaEP5w9MlRzM&state=0a19199cf14173394df29fc2e682299f
	#http://localhost:8000/FindTeammates/?code=AQTR9xUM7SuPw5xs4OVTrhjARrXWVPET5WrG3fQaDAgZsB_9HZgdFD_YFOIrn-T2vFs5i9MFGl1ZpbeVeokEyCue2wiEQH1iPILJbSYTqtZx86HUBH4&state=7873719d9118e017c81e7b9df825a6ad
	
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
	
	return redirect(authentication.authorization_url)
	'''


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
	code = request.GET.get("code")
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
	res = parser.loadPage(profile_url)
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


def afterlogin(request):
	code = request.GET.get("code")
	code=code.split("code=")[1].split("&state=")[0]
	authentication.authorization_code = code
	token=authentication.get_access_token()
	application = linkedin.LinkedInApplication(token=token)


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
	teamSize = int(request.POST.get("teamSize", 4))
	stu = Student.objects.get(id=current_id)
	course = Course.objects.get(id=current_course_id)

	team = Team(teamName=team_name, teamDescription=description, Size=teamSize, ownerID=stu, courseID=course)
	
	team.save()
	
	stu_team = student_team(studentID=stu, teamID=team)
	stu_team.save()
	return teams(request)
	#return render_to_response('FindTeammates/teams.html')

def createCourse(request):
	new_course = Course()

	'''
	if not request.user.is_authenticated():
	    return redirect('login')
	new_plan.holder = request.user
	'''

	#do validation
	new_course.University = request.POST.get('university', "")
	new_course.courseName = request.POST.get('coursename', "")
	new_course.depart_time = request.POST.get('semester', "")
	new_course.Professor = request.POST.get('professor', "")
	new_course.Capacity = request.POST.get('capacity', 50)
	new_course.groupSize = request.POST.get('groupsize', 4)
	new_course.courseDescription = ""

	new_course.save()
	return redirect("roster")


