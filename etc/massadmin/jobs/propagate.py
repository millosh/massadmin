### example job file

import sys
import time

task = 'Propagate files'
logfile = open(log_dir + '/propagate-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

cmds = [
	# copying file on every server somewhere
	{
		'type': 'local',
		'command': "scp /my/file/name.tar.gz ###FULL HOSTNAME###:/our/temporary/dir",
	},
	# connecting to the server; "access command" is ssh
	{
		'type': 'start',
		'command': '###ACCESS COMMAND### ###FULL HOSTNAME###',
	},
	# expecting server prompt and doing 'sudo -s'
	{
		'expect': server['prompt'],
		'command': 'sudo -s'
	},
	# conditional: if password is needed, type password; if we get root prompt, pass
	{
		'expect': "(?:\[sudo\] password for ###USERNAME###:)|" + server['root prompt'],
		'command': '###PASSWORD###',
		'optional': {
			'type': 'simple',
			'condition': '[sudo] password for ###USERNAME###:',
		},
	},
	# untaring
	{
		'expect': server['root prompt'],
		'command': 'tar xf /our/temporary/dir/name.tar.gz -C /final/dir',
	},
	# exiting from root
	{
		'expect': server['root prompt'],
		'command': 'exit',
	},
	# exiting from server
	{
		'expect': server['prompt'],
		'command': 'exit',
	},
]
