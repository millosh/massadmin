### example job file

import sys
import time

task = 'Testing task'
logfile = open(log_dir + '/mkusername' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

cmds = [
	{
		'type': 'start',
		'command': '###ACCESS COMMAND### -v -l ###USERNAME### ###FULL HOSTNAME###',
	},
	{
		'expect': '.+?@.+? password:',
		'command': '###PASSWORD###',
	},
	{
		'expect': server['prompt'],
		'command': 'useradd -c "Net User" -d /home/netuser -m -g users netuser',
	},
	{
		'expect': server['prompt'],
		'command': 'passwd netuser',
	},
	{
		'expect': "New UNIX password:",
		'command': "C0nnect!",
	},
	{
		'expect': "Retype new UNIX password:",
		'command': "C0nnect!",
	},
	{
		'expect': server['prompt'],
		'command': 'exit',
	},
]
