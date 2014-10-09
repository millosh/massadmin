#!/usr/bin/python

import re, os, sys, time
from os.path import *
from decimal import *
from commands import getoutput as go

company = sys.argv[1]
server = sys.argv[2]
sdate = sys.argv[3]
atype = sys.argv[4]
root_dir = "."

hourly_types = [ 'netusage', ]

var_dir = root_dir + "/var/" + company + "/" + atype
local_dir = var_dir
reports_dir = var_dir + "/reports"
if not isdir(reports_dir):
	os.system("mkdir -p \"" + reports_dir + "\"")
mount_blacklist = [ '/dev/shm', ]
system_binary = [ 'df', ]
system_decimal = [ 'netusage', ]

tm = time.strftime("%Y-%m-%d-%H-%M")

servers = {}
def netusage(servers,server,rfd,unixtime):
	content = open(rfd).read()
	rx, tx = re.findall("RX\s+bytes:(.+?)\s+\(.+?\)\s+TX\s+bytes:(.+?)\s+\(.+?\)",content)[0]
	if server not in servers:
		servers[server] = {}
	servers[server][unixtime] = {
		'rx': int(rx),
		'tx': int(tx),
	}
	return servers

def df(servers,server,rfd,unixtime):
	content = open(rfd).read()
	content = re.sub("\n\s"," ",content)
	rows = re.split("\n",content)[1:-1]
	for row in rows:
		cols = re.split("\s+",row)
		volume = cols[0]
		size = cols[1]
		used = cols[2]
		available = cols[3]
		percentage = cols[4]
		mount = cols[5]
		if mount not in mount_blacklist:
			if server not in servers:
				servers[server] = {}
			if 'df' not in servers[server]:
				servers[server]['df'] = {}
			if unixtime not in servers[server]['df']:
				servers[server]['df'][unixtime] = {}
			servers[server]['df'][unixtime][mount] = {
				'volume': volume,
				'size': int(size)*1024,
				'used': int(used)*1024,
				'available': int(available)*1024,
				'percentage': percentage,
				'mount': mount,
			}
	return servers

#mdirs = go("ls " + local_dir).split("\n")
#for server in mdirs:
fdir = local_dir + "/" + server
#if isdir(fdir):
year_dirs = go("ls " + fdir).split("\n")
for year in year_dirs:
	if atype in hourly_types:
		yd = fdir + '/' + year
		mont_dirs = go("ls " + yd).split("\n")
		for mont in mont_dirs:
			md = yd + '/' + mont
			date_dirs = go("ls " + md).split("\n")
			for date in date_dirs:
				dd = md + '/' + date
				hour_dirs = go("ls " + dd).split("\n")
				for hour in hour_dirs:
					hd = dd + '/' + hour
					hfds = go("ls " + hd + "/*.log").split("\n")
					for hfd in hfds:
						year, mont, date, hour, minu = re.findall("^.+?\-(.+?)\-(.+?)\-(.+?)\-(.+?)\-(.+?).log",hfd)[0]
						unixtime = int(time.mktime((int(year),int(mont),int(date),int(hour)+1,int(minu),0,0,0,0)))
						servers = netusage(servers,server,hfd,unixtime)
	else:
		hfds = go("ls " + fdir + "/*.log").split("\n")
		for hfd in hfds:
			year, mont, date = re.findall("^.+?-(.+?)\-(.+?)\-(.+?).log$",hfd)[0]
			unixtime = int(time.mktime((int(year),int(mont),int(date),0,0,0,0,0,0)))
			servers = df(servers,server,hfd,unixtime)

syear, smont, sday = re.split("-",sdate)
stime = int(time.mktime((int(syear),int(smont),int(sday),0+1,0,0,0,0,0)))
etime = int(time.mktime((int(syear),int(smont),int(sday)+1,0+1,0,0,0,0,0)))

if atype in [ 'netusage', ]:
	rxs = []
	txs = []
	max_rx = 0
	max_tx = 0
	t = stime
	while t <= etime:
		#t = ltimes[l]
		if t in servers[server]:
			if t-60 in servers[server]:
				rxdiff = servers[server][t]['rx']-servers[server][t-60]['rx']
				txdiff = servers[server][t]['tx']-servers[server][t-60]['tx']
			else:
				rxdiff = 0
				txdiff = 0
			cur_rx = float(rxdiff)*float(8)/float(60)
			cur_tx = float(txdiff)*float(8)/float(60)
			rxs.append(cur_rx)
			txs.append(cur_tx)
			max_rx = max(max_rx,cur_rx)
			max_tx = max(max_tx,cur_tx)
		t += 60
	max_y = max(max_rx,max_tx)

lines = {}
if atype in [ 'df', ]:
	max_y = 0
	for ut in servers[server]['df']:
		print_date = time.strftime("%Y-%m-%d",time.localtime(ut))
		out = print_date
		for mount in servers[server]['df'][ut]:
			out += ',' + str(servers[server]['df'][ut][mount]['size']) + ',' + str(servers[server]['df'][ut][mount]['used'])
			max_y = max(max_y,int(servers[server]['df'][ut][mount]['size']))
			if mount not in lines:
				lines[mount] = []
			lines[mount].append(int(servers[server]['df'][ut][mount]['used']))
		print out

# bits, kilobits, megabits...
def bkm(value,ns):
	if ns == 'binary':
		kilovalue = 1024
		megavalue = kilovalue*1024
		gigavalue = megavalue*1024
		teravalue = gigavalue*1024
		kiloadd = 'KiB'
		megaadd = 'MiB'
		gigaadd = 'GiB'
		teraadd = 'TiB'
	elif ns == 'decimal':
		kilovalue = 1000
		megavalue = kilovalue*1000
		gigavalue = megavalue*1000
		teravalue = gigavalue*1000
		kiloadd = 'Kb'
		megaadd = 'Mb'
		gigaadd = 'Gb'
		teraadd = 'Tb'
	getcontext().prec = 3
	if value > teravalue:
		string = str(Decimal(str(value))/Decimal(teravalue))
		addition = " " + teraadd
	elif value > gigavalue:
		string = str(Decimal(str(value))/Decimal(gigavalue))
		addition = " " + gigaadd
	elif value > megavalue:
		string = str(Decimal(str(value))/Decimal(megavalue))
		addition = " " + megaadd
	elif value > kilovalue:
		string = str(Decimal(str(value))/Decimal(kilovalue))
		addition = " " + kiloadd
	else:
		string = str(value)
		addition = ""
	string = string + addition
	return string

def convert_y(yv):
	# max_y:yv = 600:x
	string = str(700-int(float(yv)*float(600)/float(max_y)))
	return string

# counting top
if atype in system_binary:
	ns = 'binary'
elif atype in system_decimal:
	ns = 'decimal'
yaxis = {
	'10': bkm(max_y,ns),
	'9': bkm(float(max_y)*0.9,ns),
	'8': bkm(float(max_y)*0.8,ns),
	'7': bkm(float(max_y)*0.7,ns),
	'6': bkm(float(max_y)*0.6,ns),
	'5': bkm(float(max_y)*0.5,ns),
	'4': bkm(float(max_y)*0.4,ns),
	'3': bkm(float(max_y)*0.3,ns),
	'2': bkm(float(max_y)*0.2,ns),
	'1': bkm(float(max_y)*0.1,ns),
}
svgtemplate = reports_dir + "/image.svg"
svgout = reports_dir + "/" + server + "-" + sdate + ".svg"
pngout = reports_dir + "/" + server + "-" + sdate + ".png"
svgcontent = open(svgtemplate).read()
svgcontent = re.sub("###server###",server,svgcontent)
svgcontent = re.sub("###date###",sdate,svgcontent)
#svgcontent = re.sub("###date range###",daterange,svgcontent)
#TODO: fix this to be generic, not just fixed "year" + "mont"
svgcontent = re.sub("###date range###",year + "-" + mont,svgcontent)

if atype in [ 'netusage', ]:
	for y in yaxis:
		svgcontent = re.sub("###y" + y + "###",yaxis[y],svgcontent)
	path_rx_line  = "<path d=\"M 200 " + convert_y(rxs[0])
	path_rx_line += " L 201 " + convert_y(rxs[1])
	rx_position = 201
	for r in range(2,len(rxs)):
		rx = rxs[r]
		rx_position += 1
		path_rx_line += ", " + str(rx_position) + " " + convert_y(rx)
	path_rx_line += "\" stroke=\"blue\" fill=\"none\" stroke-width=\"1\" />"
	path_tx_line  = "<path d=\"M 200 " + convert_y(txs[0])
	path_tx_line += " L 201 " + convert_y(txs[1])
	tx_position = 201
	for t in range(2,len(txs)):
		tx = txs[t]
		tx_position += 1
		path_tx_line += ", " + str(tx_position) + " " + convert_y(tx)
	path_tx_line += "\" stroke=\"red\" fill=\"none\" stroke-width=\"1\" />"
	svgcontent = re.sub("###path rx line###",path_rx_line,svgcontent)
	svgcontent = re.sub("###path tx line###",path_tx_line,svgcontent)
#elif atype in [ 'df', ]:
#	for line in lines:
#		print line


#open(svgout,'w').write(svgcontent)
#os.system("convert \"" + svgout + "\" \"" + pngout + "\"")
