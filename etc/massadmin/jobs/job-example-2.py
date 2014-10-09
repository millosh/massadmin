### example job file

import sys
import time

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
]

arguments = [
	{
		'argument id': 'sudo password',
		'text': 'Password for sudo on Millosh: ',
		'type': 'getpass',
		'key': '###SUDO PASSWORD###',
	},
]

logfile = open(log_dir + '/aptdate_job' + time.strftime("%Y-%m-%d") + '.log','a')

### --- BREAK HERE --- ###

def test_file():
	numline = len(open(var_dir + "/aptdate-###HOSTNAME###.tmp").read().split("\n"))
	if numline == 1:
		ret = 1
	elif numline == 2:
		ret = 2
	else:
		ret = 3
	return ret

def on_value_print(string):
	print string

cmds = [
	{
		'type': 'start',
		'command': '###ACCESS COMMAND### ###FULL HOSTNAME###',
	},
	{
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
		'command': 'cat /etc/crontab | grep aptdate.sh > /tmp/aptdate-###HOSTNAME###.tmp'
	},
	{
		'expect': "(?:###HOSTNAME###.+?#)|(?:root.*?\@.*?###HOSTNAME###)",
		'command': 'exit'
	},
	{
		'expect': "(?:millosh\@.+\$)|(?:millosh.*?\@.*?###HOSTNAME###)",
		'command': 'exit'
	},
	{
		'type': 'local',
		'command': '###COPY COMMAND### ###FULL HOSTNAME###:/tmp/aptdate-###HOSTNAME###.tmp ' + var_dir,
	},
	{
		'type': 'conditional function',
		'command': 'pass',
		'condition': {
			'function': test_file,
			'values': {
				1: {
					'type': 'string',
					'command': 'print',
					'string': "###HOSTNAME###: nema",
				},
				2: {
					'type': 'string',
					'command': on_value_print,
					'string': "###HOSTNAME###: ima",
				},
				3: {
					'type': 'string',
					'command': 'print',
					'string':  "###HOSTNAME###: SOMETHING FISHING THERE!",
				},
			},
		},
	},
]
