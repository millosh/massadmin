### example job file

import sys
import time
from os.path import *

task = 'Testing task'
logfile = open(log_dir + '/scp-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

sshtype = sys.argv[3]
fd_from = sys.argv[4]
ldr = sys.argv[5]

if not isdir(ldr + '/' + server['hostname']):
	os.system("mkdir -p \"" + ldr + "/" + server['hostname'] + "\"")

pre_cmds = []
post_cmds = []
cmds = [
	{
		'type': 'run scp',
		'command': "scp " + server['username'] + "@" + server['full hostname'] + ":" + fd_from + " \"" + ldr + "/" + server['hostname'] + "\"",
	},
]

if sshtype == 'pass':
	cmds[0]['expect'] = "password:"
	cmds[0]['password'] = server['password']
