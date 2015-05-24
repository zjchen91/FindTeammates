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
import datetime
from cookie import *
from django.contrib.auth import login
import os.path


addr = 'http://localhost:8000/'
callback_postfix = 'FindTeammates/callback'
API_KEY = '77ivy1b3bzxmlk'
API_SECRET = 'yyZCB6IvxBFinBcO'
RETURN_URL = addr+ callback_postfix

BASE = os.path.dirname(os.path.abspath(__file__))



def roster(request, courseID="0"):

	template = loader.get_template('FindTeammates/roster.html')
	user = request.user
	current_student = Student.objects.all().get(user=user.id)
	current_id = current_student.id

	student_course_list = student_course.objects.filter(studentID=current_id)
	courselist = Course.objects.all().filter(id__in=student_course_list.values('courseID'))
	all_courses = Course.objects.all().exclude(id__in=courselist.values('id'))

	if len(courselist)==0:
		context = RequestContext(request, {'student_list': [], 'courselist':[], 'all_courses':all_courses})
		return HttpResponse(template.render(context))

	else:
		if courseID=="0":
			current_course_id= courselist[0].id
		else:
			current_course_id = courseID
		current_course = Course.objects.all().get(id=current_course_id)
		current_course_teams = Team.objects.all().filter(courseID=current_course_id)
		stpair = student_team.objects.all().filter(teamID__in=current_course_teams)
		studentList = student_course.objects.all().filter(courseID=current_course_id)

		alluser = []
		for stu in studentList:
			alluser.append(str(stu.studentID.id))
	
		# see whether current user is in a team or not

		# in a team
		in_team = 0
		if len(stpair.filter(studentID=current_id)) != 0:
			in_team = 1
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
				studentObjectList.append((Student.objects.get(id=int(item[0])), item[1]))

			
			context = RequestContext(request, {'student_list': studentObjectList, 'courselist':courselist, 'all_courses':all_courses, 'current_course_id':current_course_id, 'in_team':in_team, 'current_course':current_course})
			return HttpResponse(template.render(context))
		else:
			studentObjectList = []
			for s in studentList:
				studentObjectList.append((s, 'N/A'))

			context = RequestContext(request, {'student_list': studentObjectList, 'courselist':courselist, 'all_courses':all_courses, 'current_course_id':current_course_id, 'in_team':in_team, 'current_course':current_course})
			return HttpResponse(template.render(context))


def site(request):
	return render_to_response("FindTeammates/site.html")


def teams(request, courseID="0"):

	template = loader.get_template('FindTeammates/teams.html')
	user = request.user
	current_student = Student.objects.all().get(user=user.id)
	current_id = current_student.id
	student_course_list = student_course.objects.filter(studentID=current_id)
	courselist = Course.objects.all().filter(id__in=student_course_list.values('courseID'))
	all_courses = Course.objects.all().exclude(id__in=courselist.values('id'))

	
	
	if len(courselist)==0:
		context = RequestContext(request, {'team_list': [], 'courselist':[], 'all_courses':all_courses})
		return HttpResponse(template.render(context))

	else:
		if courseID=="0":
			current_course_id= courselist[0].id
		else:
			current_course_id = courseID
		current_course = Course.objects.all().get(id=current_course_id)
		stpair = student_team.objects.all()
		teamList = Team.objects.all().filter(courseID=current_course_id)
		allteam = []
		for team in teamList:
			allteam.append(str(team.id))

		in_team = 0
		# in a team
		if len(stpair.filter(studentID=current_id)) != 0:
			in_team = 1
			#print 'in a team'
			#print current_id
			teamObjectList = []
			for s in teamList:
				teamObjectList.append((s, 'N/A'))
			context = RequestContext(request, {'team_list': teamObjectList,  'courselist':courselist, 'all_courses':all_courses,  'current_course_id':current_course_id, 'current_course':current_course, 'in_team':in_team})
			return HttpResponse(template.render(context))
		else:
			#print 'alone'
			#print current_id
			preferteam = {}
			joinHis = stuJoinTeamHistory.objects.all()
			for join in joinHis:
				ner = str(join.joinerID.id)
				nee = str(join.joineeTeamID.id)
				if ner in preferteam:
					preferteam[ner].append(nee)
				else:
					preferteam[ner] = [nee]
			test = recommander(str(current_id), 'team', preferteam, allteam)
			ranklist = test.run()
			teamObjectList = []
			for item in ranklist:
				teamObjectList.append((Team.objects.get(id=int(item[0])), item[1]))
			context = RequestContext(request, {'team_list': teamObjectList, 'courselist':courselist, 'all_courses':all_courses,  'current_course_id':current_course_id, 'current_course':current_course, 'in_team':in_team})
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
	permi = linkedin.PERMISSIONS.enums.values()[:1]
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, permi)

	code = request.GET.get("code")
	authentication.authorization_code = code
	t = authentication.get_access_token()
	linkin_App = linkedin.LinkedInApplication(token=t)

	# ~~~~~~~~~~~~~~~~~~get token~~~~~~~~~~~~~~~~
	profile = linkin_App.get_profile()
	profile_url = profile['siteStandardProfileRequest']['url']
	print profile_url

	# ~~~~~~~~~~~~~~~~~~~~get info from basic_profile~~~~~~~~~~~~
	profile_id = profile['id']
	profile_name = profile['firstName'] + ' ' + profile['lastName']
	profile_headline = profile['headline']
	skills = []					# default skills and pic in case the parse fail
	profile_pic = ''
	##~~~~~~~~~~ here is the code of parser, or you can call it opener~~~~~~~~~~~
	with open(os.path.join(BASE, 'account.txt')) as f:
		username = f.readline().split('=')[1].strip(' \t"')
		password = f.readline().split('=')[1].strip(' \t"')
	parser = LinkedInParser(username, password)
	res = parser.loadPage(profile_url)

	## res contains all the full_profile, here I only parse the skills.
	## Give me a list of things need to be parsed
	## ~~~~~~~~~~~here is the code to parse profile_pic~~~~~~~~~~~~~~~
	try:
		m = re.findall('"profile-picture".+jpg\' width', res)[0]
		print "m"
		print m
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
	post = {'profile_id':profile_id,
			'name':profile_name,		#Enrui Liao
			'skill':skills,				#['Matlab','Java']
			'image':profile_pic,		#(str)
			'url':profile_url,			#(str)
			'headline':profile_headline	#(str)
			}
	print "profile id"
	print profile_id
	current_student = Student.objects.all().filter(profile_id=profile_id)
	current_user = None
	if len(current_student)==1:
		current_student = current_student[0]
		current_user = current_student.user
		current_student.name = profile_name
		current_student.skill = skills
		current_student.image = profile_pic
		current_student.headline = profile_headline
		current_student.url = profile_url
		current_student.save()
	else:
		current_user = User(is_superuser=0, is_staff=0, is_active=1, date_joined=datetime.datetime.now(), username=profile_id)
		current_user.save()
		if profile_pic.strip()=="":
			profile_pic = "../../static/FindTeammates/img/default_student_image.png"
		current_student = Student(user=current_user, name=profile_name, skill=skills, image=profile_pic, url=profile_url, headline=profile_headline, profile_id=profile_id)
		current_student.save()

	current_user.backend = 'django.contrib.auth.backends.ModelBackend'
	login(request, current_user)
	print post
	## ~~~~~~~~~~~~~~~~~~response whatever data~~~~~~~~~~~~~~~~~~~~~~~~~~
	return redirect("roster")

# redirect the browser to Linkedin login page
def site_login(request):

	permi = linkedin.PERMISSIONS.enums.values()[:1]
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, permi)
	url = authentication.authorization_url	
	return redirect(url)


def updateInviteHistory(request):
	user = request.user
	current_student = Student.objects.all().get(user=user.id)
	current_id = current_student.id
	if request.POST.has_key('client_response'):
		inviteeID = request.POST['client_response']
		inviter = Student.objects.get(id=current_id)
		invitee = Student.objects.get(id=inviteeID)
		his = teamInviteStuHistory(inviterID=inviter, inviteeID=invitee)
		his.save()
		current_course_id = request.POST['current_course_id']
		print "current_course_id"
		print current_course_id
		
		all_teams_in_current_course = Team.objects.all().filter(courseID=current_course_id)
		inviter_stu_team = student_team.objects.all().filter(studentID=inviter).filter(teamID__in=all_teams_in_current_course.values('id'))
		inviter_team = Team.objects.all().filter(id__in=inviter_stu_team.values('teamID'))
		if not len(inviter_team)==1:
			print "heere1"
			return None
		else:
			print "heere2"
			m = Message(senderID=inviter, receiverID=invitee, messageType=5, messageStatus=0, content="", teamID=inviter_team[0], date=datetime.datetime.now())
			print "here4"
			m.save()
			print "here3"
		
		return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))
	else:
		return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))

def updateJoinHistory(request):
	user = request.user
	current_student = Student.objects.all().get(user=user.id)
	current_id = current_student.id
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
	user = request.user
	current_student = Student.objects.all().get(user=user.id)
	current_id = current_student.id
	student_course_list = student_course.objects.filter(studentID=current_id)
	courselist = Course.objects.all().filter(id__in=student_course_list.values('courseID'))
	current_course_id = courselist[0].id


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

def registerCourse(request):
	courseid = request.POST.get('choosecourse',"")
	user = request.user
	current_student = Student.objects.all().get(user=user)
	current_course = Course.objects.all().get(id=courseid)
	sc = student_course(studentID=current_student, courseID=current_course)
	sc.save()
	return redirect("roster")

def showMessages(request):
	user = request.user
	current_student = Student.objects.all().get(user=user.id)
	current_id = current_student.id

	student_course_list = student_course.objects.filter(studentID=current_id)
	courselist = Course.objects.all().filter(id__in=student_course_list.values('courseID'))
	all_courses = Course.objects.all().exclude(id__in=courselist.values('id'))

	template = loader.get_template('FindTeammates/messages.html')

	current_course_id = courselist[0].id
	message_list = Message.objects.all().filter(receiverID=current_id)
	context = RequestContext(request, {'courselist':courselist, 'all_courses':all_courses, 'current_course_id':current_course_id, 'message_list':message_list})
	return HttpResponse(template.render(context))

def team_detail(request, teamID):
	user = request.user
	current_student = Student.objects.all().get(user=user.id)
	current_id = current_student.id

	student_course_list = student_course.objects.filter(studentID=current_id)
	courselist = Course.objects.all().filter(id__in=student_course_list.values('courseID'))
	all_courses = Course.objects.all().exclude(id__in=courselist.values('id'))
	current_course_id = courselist[0].id

	team = Team.objects.all().get(id=teamID)
	stu_teams = student_team.objects.all().filter(teamID=teamID)
	team_members = Student.objects.all().filter(id__in=stu_teams.values('studentID'))
	template = loader.get_template('FindTeammates/team_detail.html')
	context = RequestContext(request, {'team':team, 'team_members':team_members, 'courselist':courselist, 'all_courses':all_courses, 'current_course_id':current_course_id})
	return HttpResponse(template.render(context))


