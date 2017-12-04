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