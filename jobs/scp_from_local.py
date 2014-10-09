### example job file

import sys
import time
from os.path import *

task = 'Testing task'
logfile = open(log_dir + '/scp-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

fd_from = sys.argv[3]
ldr = sys.argv[4]
sshtype = sys.argv[5]

if not isdir(ldr):
	os.system("mkdir -p \"" + ldr + "\"")

pre_cmds = []
post_cmds = []
cmds = [
	{
		'type': 'local',
		'command': "scp \"" + fd_from + "\" " + server['full hostname'] + ":" + ldr,
	},
]

if sshtype == 'pass':
	cmds.append({
		'expect': "password",
		'command': '<my pass>',
		'optional': {
			'type': 'simple',
			'condition': 'password',
		},
	})

