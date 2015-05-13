from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response

from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import socket

def LinkedIn_login(request):
	'''
	TODO:
	get the user's ID
	get the course ID
	'''
	context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('FindTeammates/login.html',context_instance=context)



def roster(request):
	return render_to_response('FindTeammates/roster.html', context_instance=RequestContext(request))

def teams(request):
	return render_to_response('FindTeammates/teams.html')

def main(request):
	return render_to_response('FindTeammates/test.html', context_instance=RequestContext(request))

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




