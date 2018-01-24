#!/use/bin/python
# -*- coding:utf-8 -*- -
import requests,re,threading,argparse,chardet,random,sys
from urlparse import urljoin
from bs4 import BeautifulSoup

#|[root@AdminSS ~]# python KarScan.py -url http://www.site.con -file filename.txt

parser = argparse.ArgumentParser()
parser.add_argument('-url')
parser.add_argument('-file')
args = parser.parse_args()
lock = threading.Lock() #线程锁
r = requests.session()
url = args.url
subdict = []
USER_AGENTS = [
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
]
fileName = args.file 
bak = ['swp','bak','tmp','~']
press = ['zip','rar','tar.gz','7z','tar','cab','tgz','gz','bz2','z']
if 'http://' in url:
	urlc = url.replace('http://', '')
	urlc = urlc.replace('/', '')
start = '''
_______Code:4dmin55_______________________
 _  __             _____                 
 | |/ /            / ____|                
 | ' / __ _ _ __  | (___   ___ __ _ _ __  
 |  < / _` | '__|  \___ \ / __/ _` | '_ \ 
 | . \ (_| | |     ____) | (_| (_| | | | |
 |_|\_\__,_|_|    |_____/ \___\__,_|_| |_|
_________ ______ ___ _________ _____ _____
'''
print start
#初始化
class KarScan:
	def __init__(self,action,urls,filename,url,newurl):
		self.action = action
		self.urls = urls
		self.filename = filename
		self.url = url
		self.newurl = newurl


	#随机头
	def random_Headers(self=True):
		try:
			if self.action:
				headers = {
					'User-Agent': random.choice(USER_AGENTS),
					'X_FORWARDED_FOR': '%d.%d.%d.%d' % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254)),
					'Cookie':'whoami=Kar.Scan Code by 4dmin55'
				}
				print u'[++]生成随机HTTP头成功！'
				return headers
			else:
				pass
		except:
			print u'[!!]生成随机HTTP头失败！'


	#根据域名生成字典
	def fieldDict(self):
		try:
			urlq = self.urls.split('.')
			for x in range(len(press)):
				for i in range(len(urlq)-1):
					subdict.append(str(urlq[i])+'.'+str(press[x]))
					subdict.append("".join(urlq[:-1])+'.'+str(press[x]))
					subdict.append("".join(urlq)+'.'+str(press[x]))
					subdict.append(url+'.'+str(press[x]))
			print u'[++]生成域名字典成功！'
			return  subdict
		except:
			print u'[!!]生成域名字典失败！'


	#导入字典
	def bakDict(self):
		try:
			for line in open(self.filename,'r'):
				subdict.append(line.strip('\n').decode('gbk'))
			print u'[++]导入字典成功！'
			return subdict
		except:
			print u'[!!]导入字典失败！'
	

	#一级页面爬虫
	def crawlerDict(self):
		try:
			Crawler = []
			r = requests.session()
			html = r.get(self.url).text
			soup = BeautifulSoup(html,"html.parser")
			findA = soup.find_all('a')
			for x in range(len(findA)):
				if '://' in findA[x]['href']:
					url = urlparse.urlsplit(findA[x]['href'])
					if url.netloc == self.newurl:
						if url.path == '/':
							pass
						else:
							Crawler.append(url.path)
				else:
					Crawler.append(findA[x]['href'])
			tmpone = []
			tmptwo = []
			for x in range(len(Crawler)):
				if '.' in Crawler[x]:
					tmpone.append(Crawler[x]) #目录
				else:
					tmptwo.append(Crawler[x]) #文件
			for x in range(len(tmpone)):
				if "#" in tmpone[x]:
					ac =  tmpone[x].split('#')
					for i in range(len(bak)):
						if bak[i] == '~':
							subdict.append(ac[-2]+bak[i])
						else:
							subdict.append(ac[-2]+'.'+bak[i])
				elif "?" in tmpone[x]:
					ac =  tmpone[x].split('#')
					print ac[-2]
				else:
					pass
			for x in range(len(tmptwo)):
				if tmptwo[x] == '/':
					pass
				elif '/' in tmptwo[x]:
					new = tmptwo[x].split('/')
					for u in range(len(press)):
						subdict.append(tmptwo[x]+new[-2]+'.'+press[u])
				else:
					pass
				print u'[++]爬虫生成字典成功！'
		except:
			print u'[!!]爬虫生成字典失败！'


y = KarScan(True,urlc,fileName,url,urlc)
y.fieldDict()
y.bakDict()
#y.crawlerDict()
Head = y.random_Headers()


#Low B Scan 启动!
def AdminSS(url):
    try:
        r = requests.get(url,timeout=10,headers=Head)
        if r.status_code == 200:
            lock.acquire()
            print "[++] Bak FileName: %s" % url
            lock.release()
    except:
        lock.acquire()
        pass
        lock.release()


pool = []
for x in range(len(subdict)):
	site = urljoin(url,subdict[x])
	if len(pool) > 50:
		for t in pool:
			t.start()
		for t in pool:
			t.join()
		pool = []
	pool.append(threading.Thread(target=AdminSS,args=(site, )))
	sys.stdout.write(u'[++]扫描进度 %s/%s'%(str(x),str(len(subdict)-1)+'\r'))
	sys.stdout.flush()
else:
	for t in pool:
		t.start()
	for t in pool:
		t.join()















