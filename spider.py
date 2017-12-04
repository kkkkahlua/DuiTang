import requests
import re
import urllib.parse
from shell import Shell
from strproc import StrProc
from bloomfilter import BloomFilter

class Spider():
	num = 0

	def __init__(self):
		pass

	def save_picture(self, src):
		content = requests.get(src).text
		pattern = re.compile('"photo".*?"path":"(.*?)"},"msg":"(.*?)"', re.S)
		results = re.findall(pattern, content)

		for result in results:
			url,name = result

			if (bloomfilter.find(url)): return
			bloomfilter.insert(url)

			self.num = self.num + 1
			print('ok %d' % self.num)			

			if (self.num % 5 == 0):
				bloomfilter.save()
				bloomfilter.load()

			shell.save(strproc.del_spec(name),url)



	def album_proc(self, result):
		id,album = result
		album = strproc.del_spec(album)
		print(id,album)
		shell.mkdir('album\\'+album)
		shell.cd('album\\'+album)
		self.dfs_album('https://www.duitang.com/napi/blog/list/by_album/?album_id='+id+'&limit=24&include_fields=top_comments%2Cis_root%2Csource_link%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Creply_count&start=24')
		shell.cd('')

	def dfs_all(self, src, type):
		#print(src)
		if (type == 1):
			self.save_picture(src)
		elif (type == 2):
			
			content = requests.get(src).text
			pat_alb = re.compile('"album":{"id":(.*?),"name":"(.*?)"')
			results = re.findall(pat_alb, content)

			for result in results:
				self.album_proc(result)
			
			self.save_picture(src)

		content = requests.get(src).text
		pat_num = re.compile('}],"more":(.*?),"limit"')
		s_num = re.search(pat_num, content)
		if (s_num is None): return
		num = int(s_num.group(1))
		#print(num)
		if (num != 0): self.dfs_all(strproc.next(src), type)


	#	func:	save all pictures in the designated album
	#	notice: albums do not contain urls that point to other websites,
	#			as a result, dfs will end here
	def dfs_album(self, src):
		print(src)
		self.dfs_all(src, 1)

	def dfs_search(self, src):
		self.dfs_all(src, 2)


	def work(self, src):
		content = requests.get(src).text

		#	category
		pattern1 = re.compile('<a href="/category(.*?)">(.*?)</a>', re.S)
		results1 = re.findall(pattern1, content)

		for result in results1:
			url,category = result
			category = re.sub('\s', '', category)
			print(url, category)

		print('')

		'''
		#	album
		pattern2_1 = re.compile('href="/album/\?id=(.*?)".*?lstitle">(.*?)</span>', re.S)
		results2_1 = re.findall(pattern2_1, content)		
		pattern2_2 = re.compile('class="section-title" href="/album/\?id=(.*?)">(.*?)</a>', re.S)
		results2_2 = re.findall(pattern2_2, content)
		results2 = results2_1 + results2_2
		
		for result in results2:
			self.album_proc(result)
		
		print('')
		'''

		#	search
		pattern3 = re.compile('<a target=".*?href=".*?search(.*?)">(.*?)</a>', re.S)
		results3 = re.findall(pattern3, content)

		for result in results3:
			url, name = result
			name = re.sub('\s', '', name)
			print(url, name)
			shell.mkdir('search\\'+name)
			shell.cd('search\\'+name)
			self.dfs_search('https://www.duitang.com/napi/blog/list/by_search/?kw='+urllib.parse.quote(name)+'&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&_type=&start=24')
			shell.cd('')
	



spider = Spider()
shell = Shell()
strproc = StrProc()
bloomfilter = BloomFilter()
spider.work("https://www.duitang.com")
bloomfilter.save()