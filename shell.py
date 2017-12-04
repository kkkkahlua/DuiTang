import os
import requests
import re

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
		fname = name
		img = requests.get(path)
		f = open(fname[0:20] + '.jpeg', 'ab')
		f.write(img.content)
		f.close()
