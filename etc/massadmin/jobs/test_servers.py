### example job file

import sys
import time

task = 'Testing task'
logfile = open(log_dir + '/test_servers-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

cmds = [
	{
		'type': 'start',
		'command': '###ACCESS COMMAND### ###FULL HOSTNAME###',
	},
	{
		'expect': server['prompt'],
		'command': 'sudo -s'
	},
	{
		'expect': "(?:\[sudo\] password for ###USERNAME###:)|" + server['root prompt'],
		'command': '###PASSWORD###',
		'optional': {
			'type': 'simple',
			'condition': '[sudo] password for ###USERNAME###:',
		},
	},
	{
		'expect': server['root prompt'],
		'command': 'ls',
	},
	{
		'expect': server['root prompt'],
		'command': 'exit',
	},
	{
		'expect': server['prompt'],
		'command': 'exit',
	},
]
