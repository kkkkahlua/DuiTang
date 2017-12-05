import re
class StrProc():
	def __init__(self):
		pass

	def del_spec(self, title):
		title = re.sub('\s', '', title)
		x = max(title.find('\\'),title.find('/'),title.find(':'),title.find('*'),title.find('?'),title.find('"'),title.find('<'),title.find('>'),title.find('|'))
		while (x != -1):
			temp = title[0:x] + title[x+1:len(title)]
			title = temp
			x = max(title.find('\\'),title.find('/'),title.find(':'),title.find('*'),title.find('?'),title.find('"'),title.find('<'),title.find('>'),title.find('|'))
		#print(title)
		return title[0:20]

	def next_url(self, s):
		pat = 'start'
		p = s.find(pat)
		x = int(s[p+6:len(s)])
		x += 24
		temp = s[0:p+6] + str(x)
		#print(temp)
		return temp

	def next_name(self, s):
		i = len(s) - 1
		flag = False;
		while (i >= 0):
			if (ord(s[i])-ord('0') >= 0 and ord(s[i])-ord('0') <= 9):
				i -= 1
			else:
				if (s[i] == '_'):
					flag = True
				break

		if (flag == True and i != len(s) - 1):
			x = int(s[i+1:len(s)])
			x = x + 1
			ret = s[0:i+1] + str(x)
		else:
			ret = s + '_0'
		return ret

	def suffix(self, s):
		i = len(s) - 1
		while (i >= 0):
			if (s[i] == '.'): break
			else: i = i - 1
		return s[i+1:len(s)]

	def url_change(self, s):
		suf = self.suffix(s)
		pat = '.thumb'
		p = s.find(pat)
		return s[0:p] + '.' + suf