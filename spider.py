import requests
import re
from shell import Shell
from strproc import StrProc

class Spider():
	def __init__(self):
		pass

	def save_picture(self, src):
		content = requests.get(src).text
		pattern = re.compile('"photo".*?"path":"(.*?)"},"msg":"(.*?)"', re.S)
		results = re.findall(pattern, content)

		for result in results:
			url,name = result
			shell.save(strproc.del_spec(name),url)

	def dfs_all(self, src):
		print(src)
		self.save_picture(src)

		content = requests.get(src).text
		pat_num = re.compile('}],"more":(.*?),"limit"')
		num = int(re.search(pat_num, content).group(1))
		print(num)
		if (num != 0): self.dfs_all(strproc.next(src))


	#	func:	save all pictures in the designated album
	#	notice: albums do not contain urls that point to other websites,
	#			as a result, dfs will end here
	def dfs_album(self, src):
		self.dfs_all(src)

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

		#	album
		pattern2_1 = re.compile('href="/album/\?id=(.*?)".*?lstitle">(.*?)</span>', re.S)
		results2_1 = re.findall(pattern2_1, content)		
		pattern2_2 = re.compile('class="section-title" href="/album/\?id=(.*?)">(.*?)</a>', re.S)
		results2_2 = re.findall(pattern2_2, content)
		results2 = results2_1 + results2_2
		
		for result in results2:
			id,album = result
			album = re.sub('\s', '', album)
			print(id,album)
			shell.mkdir('album\\'+album)
			shell.cd('album\\'+album)
			self.dfs_album('https://www.duitang.com/napi/blog/list/by_album/?album_id='+id+'&limit=24&include_fields=top_comments%2Cis_root%2Csource_link%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Creply_count&start=24')
			shell.cd('')
		
		print('')

		#	search
		pattern3 = re.compile('<a target=".*?href=".*?search(.*?)">(.*?)</a>', re.S)
		results3 = re.findall(pattern3, content)

		for result in results3:
			url, name = result
			name = re.sub('\s', '', name)
			print(url, name)
	



spider = Spider()
shell = Shell()
strproc = StrProc()
spider.work("https://www.duitang.com")