import requests
import re
import time
import urllib.parse
from shell import Shell
from strproc import StrProc
from bloomfilter import BloomFilter

class Spider():
	num = 0
	visit = 0
	save_t = 2
	break_t = 4

	def __init__(self):
		self.num = self.visit = 0

	def save_picture(self, url, name):
		if (bloomfilter.find(url, 0)): 
			print(strproc.del_spec(name))
			print('Already visited!')
			print('')
			self.visit = self.visit + 1
			return
		bloomfilter.insert(url, 0)

		shell.save(strproc.del_spec(name),url)

		self.num = self.num + 1
		print('ok! %d' % self.num)		
		print('')

		if (self.num % self.save_t == 0):
			time_t = time.clock()
			bloomfilter.save(self.num, time_t - time_s)
			#bloomfilter.load()

		if (self.num == self.break_t):
			time_t = time.clock()
			bloomfilter.save(spider.num, time_t - time_s)

			print('get: ', spider.num)
			print('time: ', time_t - time_s)
			print('duplicate: ', spider.visit)			
			exit(0)

	def save_pictures(self, src, type, name, page_type):
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
		if (page_type == 0):
			pattern = re.compile('<img data-rootid=.*?alt="(.*?)".*?src="(.*?)"', re.S)
		else:
			pattern = re.compile('"photo".*?"path":"(.*?)"},"msg":"(.*?)"', re.S)
		results = re.findall(pattern, content)

		if (page_type == 0):
			for result in results:
				name, url = result
				url = strproc.url_change(url)
				self.save_picture(url, name)
		else:
			for result in results:
				url,name = result
				self.save_picture(url, name)


	def dfs_page(self, src, type, name):
		self.save_pictures(src, type, name, 0)

	def dfs_all(self, src, type, name):
		#print(src)
		self.save_pictures(src, type, name, 1)
		if (type != 1):		
			content = requests.get(src).text
			pat_alb = re.compile('"album":{"id":(.*?),"name":"(.*?)"', re.S)
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
		self.dfs_page('https://www.duitang.com/category'+src, 0, cname+'\\main')
		self.dfs_all('https://www.duitang.com/napi/blog/list/by_filter_id/?include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&filter_id='+urllib.parse.quote(cname)+'&start=24', 0, cname+'\\main')

		content = requests.get('https://www.duitang.com/category'+src).text
		pattern = re.compile('a href="/category'+src+'&(.*?)">(.*?)</a>', re.S)
		results = re.findall(pattern, content)

		for result in results:
			sub,sname = result
			self.dfs_page('https://www.duitang.com/category'+src+'&sub='+urllib.parse.quote(cname)+'_'+urllib.parse.quote(sname), 0, cname+'\\'+sname)
			self.dfs_all('https://www.duitang.com/napi/blog/list/by_filter_id/?include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&filter_id='+urllib.parse.quote(cname)+'_'+urllib.parse.quote(sname)+'&start=24', 0, cname+'\\'+sname)

	def dfs_album(self, src, name):
		self.dfs_page('https://www.duitang.com/album/?id='+src, 1, name)
		self.dfs_all('https://www.duitang.com/napi/blog/list/by_album/?album_id='+src+'&limit=24&include_fields=top_comments%2Cis_root%2Csource_link%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Creply_count&start=24', 1, name)

	def dfs_search(self, src, name):
		self.dfs_page('https://www.duitang.com/search/?kw='+urllib.parse.quote(name)+'&type=feed', 2, name)
		self.dfs_all('https://www.duitang.com/napi/blog/list/by_search/?kw='+src+'&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&_type=&start=24', 2, name)


	def category_proc(self, result):
		url,category = result
		category = re.sub('\s', '', category)
		print(url, category)
		self.dfs_category(url, category)		

	def album_proc(self, result):
		id,album = result
		album = strproc.del_spec(album)

		if (bloomfilter.find(album, 1)):
			print('Album already visited this time!')
			print('')
			return
		bloomfilter.insert(album, 1)

		print(id,album)
		self.dfs_album(id, album)

	def search_proc(self, result):
		url, name = result
		name = re.sub('\s', '', name)
		print(url, name)
		self.dfs_search(urllib.parse.quote(name), name)


	def work(self, src):
		content = requests.get(src).text
		
		#	category
		pattern1 = re.compile('<a href="/category(.*?)">(.*?)</a>', re.S)
		results1 = re.findall(pattern1, content)

		for result in results1:
			self.category_proc(result)

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
			self.search_proc(result)

	


time_s = time.clock()

spider = Spider()

shell = Shell()

strproc = StrProc()

bloomfilter = BloomFilter()

spider.work("https://www.duitang.com")

