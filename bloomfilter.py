import os

class BloomFilter():
	mod = 786433
	l = list(range(786433))

	def load(self):
		if (os.path.exists("F:\py\\Spider\\rec.txt")):
			self.l = []
			fin = open('F:\py\\Spider\\rec.txt', 'r')
			line = fin.readline()
			for c in line:
				self.l.append(ord(c)-ord('0'))
			fin.close()
		else:
			for x in self.l:
				self.l[x] = 0

	def __init__(self):
		self.load()

	def RSHash(self, s):
		b = 378551
		a = 63689
		hash = 0
		i = 0
		for c in s:
			hash = (hash * a + ord(c)) % self.mod
			a = a * b % self.mod
		return hash

	def JSHash(self, s):
		hash = 1315423911
		for c in s:
			hash = (hash ^ (((hash << 5) % self.mod) + ord(c) + (hash >> 2))) % self.mod
		return hash

	def BKDRHash(self, s):
		seed = 131
		hash = 0
		for c in s:
			hash = (hash * seed % self.mod + ord(c)) % self.mod
		return hash

	def SDBMHash(self, s):
		hash = 0
		for c in s:
			hash = ((ord(c) + (hash << 6) % self.mod + (hash << 16) % self.mod) % self.mod + self.mod - hash) % self.mod
		return hash

	def DJBHash(self, s):
		hash = 5381
		for c in s:
			hash = ((hash << 5) % self.mod + hash + ord(c)) % self.mod
		return hash

	def insert(self, s):
		x1 = self.RSHash(s)
		x2 = self.JSHash(s)
		x3 = self.BKDRHash(s)
		x4 = self.SDBMHash(s)
		x5 = self.DJBHash(s)
		self.l[x1] = self.l[x2] = self.l[x3] = self.l[x4] = self.l[x5] = 1


	def find(self, s):
		return self.l[self.RSHash(s)] & self.l[self.JSHash(s)] & self.l[self.BKDRHash(s)] & self.l[self.SDBMHash(s)] & self.l[self.DJBHash(s)]

	def save(self):
		fout = open('F:\py\\Spider\\rec.txt', 'w')
		for c in self.l: 
			if (c != 0 | c != 1):
				print(c,str(c))
			fout.write(str(c))