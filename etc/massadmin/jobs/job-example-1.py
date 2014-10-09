### example job file

import sys

task = 'Testing task'
servers = [
	{
		'server id': 'feniks.millosh.local',
		'hostname': 'feniks',
		'full hostname': 'feniks.millosh.local',
		'distribution': 'Debian',
		'version': 'sid',
	},
	{
		'server id': 'master.millosh.net',
		'hostname': 'master',
		'full hostname': 'master.millosh.net',
		'distribution': 'Debian',
		'version': 'lenny',
	},
#	{
#		'server id': 'druga',
#		'hostname': 'localhost',
#		'distribution': 'Debian',
#		'version': 'sid',
#		'remote': 'no',
#	},
]

arguments = [
	{
		'argument id': 'sudo password',
		'text': 'Password for sudo on Millosh: ',
		'type': 'getpass',
		'key': '###SUDO PASSWORD###',
	},
]

logfile = sys.stdout

### --- BREAK HERE --- ###

cmds = [
	{
		'type': 'pre-local',
		'command': "###COPY COMMAND### for_transport2.txt ###FULL HOSTNAME###:",
	},
	{
		#'expect': "(?:millosh.*?\@.*?druga)",
		'type': 'start',
		'command': '###ACCESS COMMAND### ###FULL HOSTNAME###',
	},
	{
		# 'type': 'expect' -- doesn't need
		'expect': "(?:millosh\@.+\$)|(?:millosh.*?\@.*?###HOSTNAME###)",
		'command': 'sudo -s'
	},
	{
		'expect': "(?:\[sudo\] password for millosh:)|(?:root.*?\@.*?###HOSTNAME###)",
		'command': '###SUDO PASSWORD###',
		'optional': {
			'type': 'simple',
			'condition': '[sudo] password for millosh:',
		},
	},
	{
		'expect': "(?:###HOSTNAME###.+?#)|(?:root.*?\@.*?###HOSTNAME###)",
		'command': 'netstat -nlt'
	},
	{
		'expect': "(?:###HOSTNAME###.+?#)|(?:root.*?\@.*?###HOSTNAME###)",
		'command': 'exit'
	},
	{
		'expect': "(?:millosh\@.+\$)|(?:millosh.*?\@.*?###HOSTNAME###)",
		'command': 'exit'
	},
]
