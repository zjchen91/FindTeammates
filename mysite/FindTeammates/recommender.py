
__author__='Wendan Kang <wk2269@columbia.edu>'
__date__='$Apr 25, 2015'

'''
For users already in a team, they can invite people to join their teams. And we'll recommend three types of people:
1. People who are similar to those who this user already invited
2. People who have prefered skills of the team
3. People who used to be the teammates with this userType

For users who still didn't join a team, they can ask to join several teams. And we'll recommend three types of teams:
1. Teams which are similar to those  which this user already asked to join
2. Teams whose prefered skills are similar to his/her skills 
3. Teams which their old teammates have now been in
'''


'''
TODO: 
# need a global set to store overlab of skill set
# once a new user log in
# update the overlap of skill set
teamBasedSkillSetOverlap = {teamid: {userid: numofOverlap, userid: numofOverlap...}, teamid: ...}
userBasedSkillSetOverlap = {userid: {teamid: numofOverlap, teamid: numofOverlap...}, userid: ...}

update condition:
1. new user register
2. user joint a team, remove the userid from teamBasedSkillSetOverlap['teamID']
3. user joint a team, remove the teamid from userBasedSkillSetOverlap['userid']
'''


import sys
import math
import operator


class recommander:
	userID = ''
	# type = 'team' or 'user'
	userType = ''
	preferDataSet = {}
	oldTeammates = []
	

	def __init__(self, uid, utype, preferDataSet, alldata):
		self.userID = uid
		self.userType = utype
		self.preferDataSet = preferDataSet
		self.alldata = alldata
		#self.oldTeammates = oldTeammates


	# preferDataSet: {id: [ids id endorsed]} for user in team
	# preferDataSet: {id: [team id]} for user not in team
	def itemBasedCF(self):
		C = dict()
		N = dict()
		for user in self.preferDataSet:
			users = self.preferDataSet[user]
			#print 'hi,', user, ': ', users
			for i in users:
				N.setdefault(i,0)
				N[i] += 1
				C.setdefault(i,{})
				for j in users:
					if i == j:
						continue
					C[i].setdefault(j,0)
					C[i][j] += 1
		self.W = dict()
		for i,related_items in C.items():
			self.W.setdefault(i,{})
			for j,cij in related_items.items():
				self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))

	def CFScore(self):
		self.rankCF = dict()
		items = self.preferDataSet[self.userID]
		for i in xrange(len(items)):
			for j,wj in self.W[items[i]].items():
				if j in items or j == self.userID:
					continue
				self.rankCF.setdefault(j,0)
				self.rankCF[j] += (100 - i) * wj
		self.rankCF = normalize(self.rankCF)

		# normalize self.rankCF
		#return dict(sorted(self.rankCF.items(),key=lambda x:x[1],reverse=True))
	'''
	def skillSetScore(self):
		global teamBasedSkillSetOverlap
		global userBasedSkillSetOverlap
		self.rankSS = dict()
		if self.userType == 'team':
			teamID = getTeamId(self.userID)
			try:
				userPreferred = teamBasedSkillSetOverlap[teamID]
				print '??', userPreferred
				self.rankSS = normalize(userPreferred)
			except:
				print 'error'
		else:
			#print 'what?', self.userType
			try:
				userPreferred = userBasedSkillSetOverlap[self.userID]
				self.rankSS = normalize(userPreferred)
			except:
				print 'error'
		self.rankSS = normalize(self.rankSS)


	def oldTeammatesScore(self, weight):
		self.rankOT = dict()
		if self.userType == 'team':
			for user in self.oldTeammates:
				self.rankOT.setdefault(user, weight)
				self.rankOT[user] += weight
			self.rankOT = normalize(self.rankOT)
		else:
			for user in self.oldTeammates:
				teamID = getTeamId(user)
				self.rankOT.setdefault(teamID, weight)
				self.rankOT[teamID] += weight
			self.rankOT = normalize(self.rankOT)
	'''

	def recommend(self):
		rank = {}
		for user in self.rankCF:
			rank.setdefault(user, 0)
			rank[user] += self.rankCF[user]
		'''
		for user in self.rankSS:
			rank.setdefault(user, 0)
			rank[user] += self.rankSS[user]
		
		for user in self.rankOT:
			rank.setdefault(user, 0)
			rank[user] += self.rankOT[user]
		'''
		rank = sorted(rank.items(),key=lambda x:x[1],reverse=True)
		ranklist = []
		for item in rank:
			ranklist.append(item[0])
		for item in self.alldata:
			if (item not in ranklist) and (item != self.userID):
				ranklist.append(item)
		return ranklist

	def run(self):
		self.itemBasedCF()
		self.CFScore()
		#print 'CF:', self.rankCF
		#self.skillSetScore()
		#print 'skill:', self.rankSS
		#self.oldTeammatesScore(10)
		#print 'old:', self.rankOT
		return self.recommend()




def normalize(d):
	s = math.fsum(d.itervalues())
	if s == 0:
		return d
	factor=100.0/math.fsum(d.itervalues())
	for k in d:
		d[k] = d[k] * factor
	key_for_max = max(d.iteritems(), key=operator.itemgetter(1))[0]
	diff = 100.0 - math.fsum(d.itervalues())
	d[key_for_max] += diff
	return d

def getTeamId(userID):
	return 't' + userID



'''
if __name__ == '__main__':
	uid = '1'
	utype = 'team'
	
	preferuser = {'1':['2', '4', '6'], '2': ['3', '4', '6'], '3':[], '4': ['3'], '5':['2', '4', '3'], '6':['1', '2', '3']}
	#preferuser = {'1':['2', '3'], '3': ['2', '1'], '2':['3', '1']}
	preferteam = {'1':['t1', 't3', 't5'], '2':[], '3': ['t3', 't1'], '4':['t1', 't4'], '5':[], '6':[]}
	#teamBasedSkillSetOverlap = {}
	#userBasedSkillSetOverlap = {}
	teamBasedSkillSetOverlap = {'t1': {'4': 3}, 't2': {'4': 2, '6': 3}}
	userBasedSkillSetOverlap = {'1': {'t1' : 5}, '2':{'t2': 3}, '3':{}, '4': {'t1': 3, 't2': 2}, '5':{}, '6':{'t2':3}}
	test = recommander(uid, utype, preferuser)
	print test.run()
'''














