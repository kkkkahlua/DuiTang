import os

class BloomFilter():
	mod = [7340033,786433]

	#	if visited ever, never again visit
	l_url = list(range(7340033))
	#	if visited, not check again in this run
	l_alb = list(range(786433))

	item = 0
	elapse = 0

	def load(self):
		if (os.path.exists("F:\py\\Spider\\rec.txt")):
			self.l_url = []
			fin = open('F:\py\\Spider\\rec.txt', 'r')
			line = fin.readline()
			for c in line:
				self.l_url.append(ord(c)-ord('0'))
			fin.close()
		else:
			for x in self.l_url:
				self.l_url[x] = 0

		if (os.path.exists('F:\py\\Spider\\runtime.txt')):
			fin = open('F:\py\\Spider\\runtime.txt', 'r')
			self.item = int(fin.readline())
			self.elapse = float(fin.readline())
		else:
			self.item = self.elapse = 0
		print(self.item)
		print(self.elapse)

	def __init__(self):
		for x in self.l_alb:
			self.l_alb[x] = 0
		self.load()

	def RSHash(self, s, type):
		b = 378551
		a = 63689
		hash = 0
		i = 0
		for c in s:
			hash = (hash * a + ord(c)) % self.mod[type]
			a = a * b % self.mod[type]
		return hash

	def JSHash(self, s, type):
		hash = 1315423911
		for c in s:
			hash = (hash ^ (((hash << 5) % self.mod[type]) + ord(c) + (hash >> 2))) % self.mod[type]
		return hash

	def BKDRHash(self, s, type):
		seed = 131
		hash = 0
		for c in s:
			hash = (hash * seed % self.mod[type] + ord(c)) % self.mod[type]
		return hash

	def SDBMHash(self, s, type):
		hash = 0
		for c in s:
			hash = ((ord(c) + (hash << 6) % self.mod[type] + (hash << 16) % self.mod[type]) % self.mod[type] + self.mod[type] - hash) % self.mod[type]
		return hash

	def DJBHash(self, s, type):
		hash = 5381
		for c in s:
			hash = ((hash << 5) % self.mod[type] + hash + ord(c)) % self.mod[type]
		return hash

	def insert(self, s, type):
		x1 = self.RSHash(s,type)
		x2 = self.JSHash(s,type)
		x3 = self.BKDRHash(s,type)
		x4 = self.SDBMHash(s,type)
		x5 = self.DJBHash(s,type)
		if (type == 0):
			self.l_url[x1] = self.l_url[x2] = self.l_url[x3] = self.l_url[x4] = self.l_url[x5] = 1
		else:
			self.l_alb[x1] = self.l_alb[x2] = self.l_alb[x3] = self.l_alb[x4] = self.l_alb[x5] = 1			

	def find(self, s, type):
		if (type == 0):
			return self.l_url[self.RSHash(s,type)] and self.l_url[self.JSHash(s,type)] and self.l_url[self.BKDRHash(s,type)] and self.l_url[self.SDBMHash(s,type)] and self.l_url[self.DJBHash(s,type)]
		else:
			return self.l_alb[self.RSHash(s,type)] and self.l_alb[self.JSHash(s,type)] and self.l_alb[self.BKDRHash(s,type)] and self.l_alb[self.SDBMHash(s,type)] and self.l_alb[self.DJBHash(s,type)]

	def save(self, num, time):
		fout = open('F:\py\\Spider\\rec.txt', 'w')
		for c in self.l_url: 
			if (c != 0 | c != 1):
				print(c,str(c))
			fout.write(str(c))

		fout = open('F:\py\\Spider\\runtime.txt', 'w')
		print(self.item+num)
		print(self.elapse+time)
		fout.write(str(self.item+num)+'\n'+str(self.elapse+time))
