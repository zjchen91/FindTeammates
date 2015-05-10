from django.db import models


class Student(models.Model):
	name = models.CharField(max_length=100)
	'''
	attributes from linkedin
	'''

class Course(models.Model):
	University = models.CharField(max_length=200)
	Professor = models.CharField(max_length=100)
	courseName = models.CharField(max_length=200)
	Capacity = models.IntegerField(default=0)
	groupSize = models.IntegerField(default=0)
	courseDescription = models.CharField(max_length=500)

class Team(models.Model):
	teamName = models.CharField(max_length=100)
	teamDescription = models.CharField(max_length=500)
	ownerID = models.ForeignKey(Student)
	#preferredSkill: bitMap
	courseID = models.ForeignKey(Course)
	'''
	Status:
	0: active
	1: finalized
	2: deleted
	'''
	Status = models.IntegerField(default=0)
	Size = models.IntegerField(default=0)

'''
not sure how we get sender, receiver and team
not sure type is completed
'''
class Message(models.Model):
	senderID = models.ForeignKey(Student, related_name='sender')
	receiverID = models.ForeignKey(Student, related_name='receiver')
	'''
	messageType:
	0: default
	1: sender asks to join receiver's team
	2: sender broadcast to finalize the team
	3: sender broadcast to delete the team
	4: system notifies receiver that he's approved to join a team
	'''
	messageType = models.IntegerField(default=0)
	content = models.CharField(max_length=200)
	'''
	messageStatus:
	0: unprocessed
	1: processed
	'''
	messageStatus = models.IntegerField(default=0)
	teamID = models.ForeignKey(Team)
	date = models.DateField()

class student_course(models.Model):
	studentID = models.ForeignKey(Student)
	courseID = models.ForeignKey(Course)

class student_team(models.Model):
	studentID = models.ForeignKey(Student)
	teamID = models.ForeignKey(Team)

'''
TODO:
database optimize:
1. index
'''
class teamInviteStuHistory(models.Model):
	inviterID = models.ForeignKey(Student, related_name='inviter')
	inviteeID = models.ForeignKey(Student, related_name='invitee')

class stuJoinTeamHistory(models.Model):
	joinerID = models.ForeignKey(Student)
	joineeTeamID = models.ForeignKey(Team)

class skillOverlap(models.Model):
	teamID = models.ForeignKey(Team)
	studentID = models.ForeignKey(Student)
	numOfOverlap = models.IntegerField(default=0)














