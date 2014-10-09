### example job file

import sys, time
from os.path import *

task = 'Get output'
logfile = open(log_dir + '/get-output-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

# command
cmd = sys.argv[3]
# remote file name
rfd = sys.argv[4]
# local dir for files
ldr = sys.argv[5]

if not isdir(ldr):
	os.system("mkdir -p \"" + ldr + "\"")

cmds = [
	{
		'expect': '\[.+?@.+? \~\]',
		'command': cmd + " > " + rfd,
	},
	{
		'type': 'run scp',
		'command': 'scp ' + server['username'] + '@' + server['full hostname'] + ':' + rfd + ' ' + ldr + '/' + server['hostname'] + ".txt",
		'expect': '.+?@.+? password:',
		'password': server['password'],
	},
	{
		'expect': '\[.+?@.+? \~\]',
		'command': 'rm -f ' + rfd,
	},
]
