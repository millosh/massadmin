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
		'prompt': '(?:millosh\@.+\$)',
		'root prompt': '(?:feniks.+?#)',
	},
	{
		'server id': 'master.millosh.net',
		'hostname': 'master',
		'full hostname': 'master.millosh.net',
		'distribution': 'Debian',
		'version': 'lenny',
		'prompt': '(?:millosh.*?\@.*?master)',
		'root prompt': '(?:root.*?\@.*?master)',
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
		ret = "doesn't have"
	elif numline == 2:
		ret = "has"
	else:
		ret = "error"
	return ret

def on_value_print(string):
	print string

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
		'expect': "(?:\[sudo\] password for millosh:)|" + server['root prompt'],
		'command': '###SUDO PASSWORD###',
		'optional': {
			'type': 'simple',
			'condition': '[sudo] password for millosh:',
		},
	},
	{
		'expect': server['root prompt'],
		'command': 'cat /etc/crontab | grep aptdate.sh > /tmp/aptdate-###HOSTNAME###.tmp'
	},
	{
		'type': 'local',
		'command': '###COPY COMMAND### ###FULL HOSTNAME###:/tmp/aptdate-###HOSTNAME###.tmp ' + var_dir + " >/dev/null",
	},
	{
		'type': 'conditional function',
		'command': '=conditional funciton',
		'condition': {
			'function': test_file,
			'values': {
				"doesn't have": {
					'type': 'command key',
					'command key': 'continue',
				},
				"has": {
					'type': 'command key',
					'command key': 'pass',
				},
				"error": {
					'type': 'string',
					'command': 'print',
					'string':  "###HOSTNAME###: SOMETHING FISHING THERE!",
				},
			},
		},
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "ls",
	},
	# prebaci
	# obrisi ako postoji u tmp-u nesto kao to
	# raspakuj u tmp
	# mkdir -p /root/tools
	# cp -a /tmp/.../* /root/tools
	# obrisi iz tmp-a
	# dodaj u krontab
	# pokreni prvi put
	{
		'command key': '(pass|continue)',
		'expect': server['root prompt'],
		'command': 'exit',
	},
	{
		'command key': '(pass|continue)',
		'expect': server['prompt'],
		'command': 'exit',
	},
]
