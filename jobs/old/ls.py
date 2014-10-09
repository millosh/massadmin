### example job file

import sys
import time

task = 'Testing task'
logfile = open(log_dir + '/test_servers-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

cmds = [
	{
		'type': 'start',
		'command': '###ACCESS COMMAND### -l ###USERNAME### ###FULL HOSTNAME###',
	},
	{
		'expect': '.+?@.+? password:',
		'command': server['password'],
	},
	{
		'expect': '\[.+?@.+? \~\]',
		'command': 'ls',
	},
	{
		'expect': '\[.+?@.+? \~\]',
		'command': 'exit',
	},
]
