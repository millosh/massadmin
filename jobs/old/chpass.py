### example job file

import sys
import time

task = 'Testing task'
logfile = open(log_dir + '/test_servers-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

cmds = [
	{
		'type': 'local',
		'command': 'echo "###HOSTNAME###;###FULL HOSTNAME###;" >> domainnames.txt',
	},
	{
		'type': 'start',
		'command': '###ACCESS COMMAND### -l ###USERNAME### ###FULL HOSTNAME###',
	},
	{
		'expect': '.+?@.+? password:',
		'command': 'C0nnect!',
	},
	{
		'expect': '\[.+?@.+? \~\]\$',
		'command': 'domainname > domainnames.txt',
	},
	{
		'expect': '\[.+?@.+? \~\]\$',
		'command': 'exit',
	},
	{
		'type': 'run scp',
		'command': 'scp ###USERNAME###@###FULL HOSTNAME###:domainnames.txt ###HOSTNAME###.txt',
		'expect': '.+?@.+? password:',
		'password': 'C0nnect!',
	},
	{
		'type': 'local',
		'command': 'cat ###HOSTNAME###.txt >> domainnames.txt',
	},
	{
		'type': 'local',
		'command': 'rm ###HOSTNAME###.txt',
	},
	{
		'type': 'start',
		'command': '###ACCESS COMMAND### -l ###USERNAME### ###FULL HOSTNAME###',
	},
	{
		'expect': '.+?@.+? password:',
		'command': 'C0nnect!',
	},
	{
		'expect': '\[.+?@.+? \~\]\$',
		'command': 'rm domainnames.txt',
	},
	{
		'expect': '\[.+?@.+? \~\]\$',
		'command': 'exit',
	},
]
