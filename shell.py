import os
import requests
import re
from strproc import StrProc

class Shell:
	def __init__(self):
		pass

	def mkdir(self, path):
		path = path.strip()
		exist = os.path.exists(os.path.join("F:\picture\duitang", path))
		if not exist:
			os.makedirs(os.path.join("F:\picture\duitang",path))
			return True
		else:
			return False

	def cd(self, path):
		path = path.strip()
		os.chdir(os.path.join("F:\picture\duitang", path))

	def save(self, name, path):
		suffix = strproc.suffix(path)
		exist = os.path.exists(name+'.'+suffix)
		while 1:
			fname = name
			if not exist:
				break
			else:
				name = strproc.next_name(name)
				exist = os.path.exists(name + '.' + suffix)

		print(fname)
		img = requests.get(path)
		f = open(fname + '.' + suffix, 'ab')
		f.write(img.content)
		f.close()

strproc = StrProc()