### example job file

import sys
import time

task = 'Testing task'
logfile = open(log_dir + '/cmd-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

cmd = sys.argv[3]

cmds = [
	{
		'expect': server['prompt'],
		'command': cmd,
	},
]

