#!/usr/bin/python

import re, os, sys, time
from os.path import *
from decimal import *
from commands import getoutput as go

company = sys.argv[1]
server = sys.argv[2]
sdate = sys.argv[3]
root_dir = "."

var_dir = root_dir + "/var/" + company + "/netusage"
local_dir = var_dir
reports_dir = var_dir + "/reports"
if not isdir(reports_dir):
	os.system("mkdir -p \"" + reports_dir + "\"")

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

#mdirs = go("ls " + local_dir).split("\n")
#for server in mdirs:
fdir = local_dir + "/" + server
#if isdir(fdir):
year_dirs = go("ls " + fdir).split("\n")
for year in year_dirs:
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

syear, smont, sday = re.split("-",sdate)
stime = int(time.mktime((int(syear),int(smont),int(sday),0+1,0,0,0,0,0)))
etime = int(time.mktime((int(syear),int(smont),int(sday)+1,0+1,0,0,0,0,0)))


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
max_rxtx = max(max_rx,max_tx)

# bits, kilobits, megabits...
def bkm(value):
	getcontext().prec = 3
	if value > 1000000:
		string = str(Decimal(str(value))/Decimal(1000000))
		addition = " Mbps"
	elif value > 1000:
		string = str(Decimal(str(value))/Decimal(1000))
		addition = " kbps"
	else:
		string = str(value)
		addition = ""
	string = string + addition
	return string

def convert_y(yv):
	# max_rxtx:yv = 600:x
	string = str(700-int(float(yv)*float(600)/float(max_rxtx)))
	return string

# counting top
yaxis = {
	'10': bkm(max_rxtx),
	'9': bkm(float(max_rxtx)*0.9),
	'8': bkm(float(max_rxtx)*0.8),
	'7': bkm(float(max_rxtx)*0.7),
	'6': bkm(float(max_rxtx)*0.6),
	'5': bkm(float(max_rxtx)*0.5),
	'4': bkm(float(max_rxtx)*0.4),
	'3': bkm(float(max_rxtx)*0.3),
	'2': bkm(float(max_rxtx)*0.2),
	'1': bkm(float(max_rxtx)*0.1),
}
svgtemplate = reports_dir + "/image.svg"
svgout = reports_dir + "/" + server + "-" + sdate + ".svg"
pngout = reports_dir + "/" + server + "-" + sdate + ".png"
svgcontent = open(svgtemplate).read()
svgcontent = re.sub("###server###",server,svgcontent)
svgcontent = re.sub("###date###",sdate,svgcontent)
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
open(svgout,'w').write(svgcontent)
os.system("convert \"" + svgout + "\" \"" + pngout + "\"")
