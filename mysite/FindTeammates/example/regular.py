import re
with open('example.html','r') as f:
	res = f.read()
skills = re.findall('data-endorsed-item-name="\w+"', res)
for i in range(len(skills)):
	skills[i] = skills[i].split('=')[1].strip('"')
print skills
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
print m[start:end]