from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response


def roster(request):
	return render_to_response('FindTeammates/roster.html')

def teams(request):
	return render_to_response('FindTeammates/teams.html')
