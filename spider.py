import requests
import re
import urllib.parse
from shell import Shell
from strproc import StrProc
from bloomfilter import BloomFilter

class Spider():
	num = 0
	save_t = 50
	break_t = 5000

	def __init__(self):
		pass

	def save_picture(self, src, type, name):
		if (type == 0):
			shell.mkdir('category\\'+name)
			shell.cd('category\\'+name)
		elif (type == 1):
			shell.mkdir('album\\'+name)
			shell.cd('album\\'+name)
		elif (type == 2):
			shell.mkdir('search\\'+name)
			shell.cd('search\\'+name)

		content = requests.get(src).text
		pattern = re.compile('"photo".*?"path":"(.*?)"},"msg":"(.*?)"', re.S)
		results = re.findall(pattern, content)

		for result in results:
			url,name = result

			if (bloomfilter.find(url, 0)): 
				print(strproc.del_spec(name))
				print('Already visited!')
				print('')
				return
			bloomfilter.insert(url, 0)

			shell.save(strproc.del_spec(name),url)

			self.num = self.num + 1
			print('ok! %d' % self.num)		
			print('')
			
			if (self.num % self.save_t == 0):
				bloomfilter.save()
				#bloomfilter.load()

			if (self.num == self.break_t):
				exit(0)


	def dfs_all(self, src, type, name):
		#print(src)
		self.save_picture(src, type, name)
		if (type != 1):		
			content = requests.get(src).text
			pat_alb = re.compile('"album":{"id":(.*?),"name":"(.*?)"')
			results = re.findall(pat_alb, content)

			for result in results:
				self.album_proc(result)

		content = requests.get(src).text
		pat_num = re.compile('}],"more":(.*?),"limit"')
		s_num = re.search(pat_num, content)
		if (s_num is None): return
		num = int(s_num.group(1))
		#print(num)
		if (num != 0): self.dfs_all(strproc.next_url(src), type, name)

	def dfs_category(self, src, cname):
		self.dfs_all('https://www.duitang.com/napi/blog/list/by_filter_id/?include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&filter_id='+urllib.parse.quote(cname)+'&start=24', 0, cname+'\\main')

		content = requests.get('https://www.duitang.com/category'+src).text
		pattern = re.compile('a href="/category'+src+'&(.*?)">(.*?)</a>')
		results = re.findall(pattern, content)

		for result in results:
			sub,sname = result
			self.dfs_all('https://www.duitang.com/napi/blog/list/by_filter_id/?include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&filter_id='+urllib.parse.quote(cname)+'_'+urllib.parse.quote(sname)+'&start=24', 0, cname+'\\'+sname)

	def dfs_album(self, src, name):
		self.dfs_all(src, 1, name)

	def dfs_search(self, src, name):
		self.dfs_all(src, 2, name)

	def album_proc(self, result):
		id,album = result
		album = strproc.del_spec(album)

		if (bloomfilter.find(album, 1)): return
		bloomfilter.insert(album, 1)

		print(id,album)
		self.dfs_album('https://www.duitang.com/napi/blog/list/by_album/?album_id='+id+'&limit=24&include_fields=top_comments%2Cis_root%2Csource_link%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Creply_count&start=24', album)

	def work(self, src):
		content = requests.get(src).text

		#	category
		pattern1 = re.compile('<a href="/category(.*?)">(.*?)</a>', re.S)
		results1 = re.findall(pattern1, content)

		for result in results1:
			url,category = result
			category = re.sub('\s', '', category)
			print(url, category)
			self.dfs_category(url, category)

		print('')

		
		#	album
		pattern2_1 = re.compile('href="/album/\?id=(.*?)".*?lstitle">(.*?)</span>', re.S)
		results2_1 = re.findall(pattern2_1, content)		
		pattern2_2 = re.compile('class="section-title" href="/album/\?id=(.*?)">(.*?)</a>', re.S)
		results2_2 = re.findall(pattern2_2, content)
		results2 = results2_1 + results2_2
		
		for result in results2:
			self.album_proc(result)
		
		print('')
		

		#	search
		pattern3 = re.compile('<a target=".*?href=".*?search(.*?)">(.*?)</a>', re.S)
		results3 = re.findall(pattern3, content)

		for result in results3:
			url, name = result
			name = re.sub('\s', '', name)
			print(url, name)
			self.dfs_search('https://www.duitang.com/napi/blog/list/by_search/?kw='+urllib.parse.quote(name)+'&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&_type=&start=24', name)
	



spider = Spider()
shell = Shell()
strproc = StrProc()
bloomfilter = BloomFilter()
spider.work("https://www.duitang.com")
bloomfilter.save()