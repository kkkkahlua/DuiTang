import re
class StrProc():
	def __init__(self):
		pass

	def del_spec(self, title):
		title = re.sub('\s', '', title)
		x = max(title.find('\\'),title.find('/'))
		while (x != -1):
			temp = title[0:x] + title[x+1:len(title)]
			title = temp
			x = max(title.find('/'), title.find('\\'))
		#print(title)
		return title[0:20]

	def next(self, s):
		pat = 'start'
		p = s.find(pat)
		x = int(s[p+6:len(s)])
		x += 24
		temp = s[0:p+6] + str(x)
		#print(temp)
		return temp