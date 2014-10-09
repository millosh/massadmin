#!/usr/bin/python

import re, os, sys, time
from os.path import *
from commands import getoutput as go

tm = time.strftime("%Y-%m-%d-%H-%M")

ma_cmd = "./massadmin.py ./servers/millosh/servers.all ./jobs/cmd.py "
ma_scp = "./massadmin.py ./servers/millosh/servers.all ./jobs/scp_from_remote.py pass "

remote_dir = sys.argv[1]
local_dir = sys.argv[2]

md_cmd = "mkdir -p " + remote_dir + "/" + tm
mv_cmd = "mv " + remote_dir + "/*.log " + remote_dir + "/" + tm
tr_cmd = "cd " + remote_dir + "; tar jcf " + tm + ".tar.bz2 " + tm + "; cd -"
al_cmd = ma_cmd + "\"" + md_cmd + '; ' + mv_cmd + '; ' + tr_cmd + "\""
print al_cmd
os.system(al_cmd)

scp_cmd = ma_scp + remote_dir + "/" + tm + ".tar.bz2 " + local_dir
print scp_cmd
os.system(scp_cmd)

rm_cmd = ma_cmd + "\"rm -rf " + remote_dir + "/" + tm + "*\""
print rm_cmd
os.system(rm_cmd)

mdirs = go("ls " + local_dir).split("\n")
for mdir in mdirs:
	fdir = local_dir + "/" + mdir
	if isdir(fdir):
		cmd = "tar xf " + fdir + "/" + tm + ".tar.bz2 -C " + fdir
		print cmd
		os.system(cmd)
		cmd = "rm " + fdir + "/" + tm + ".tar.bz2"
		print cmd
		os.system(cmd)
		ndir = fdir + "/" + tm
		fds = go("ls " + ndir + "/*.log").split("\n")
		for fd in fds:
			year, mont, date, hour, minu = re.split("\-",re.sub("^.+?\-(.+?)\.log$","\g<1>",(re.split("/",fd)[-1])))
			adir = fdir + "/" + year + "/" + mont + "/" + date + "/" + hour
			if not isdir(adir):
				cmd = "mkdir -p " + adir
				print cmd
				os.system(cmd)
			cmd = "mv " + fd + " " + adir
			print cmd
			os.system(cmd)
		cmd = "rmdir " + ndir
		print cmd
		os.system(cmd)
