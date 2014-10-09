### example job file

import sys
import time

task = 'Testing task'
logfile = open(log_dir + '/aptdate_job' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

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
		'expect': "(?:\[sudo\] password for ###USERNAME###:)|" + server['root prompt'],
		'command': '###PASSWORD###',
		'optional': {
			'type': 'simple',
			'condition': '[sudo] password for ###USERNAME###:',
		},
	},
	{
		'expect': server['root prompt'],
		'command': 'cat /etc/crontab | grep aptdate.sh > /tmp/aptdate-###HOSTNAME###.tmp'
	},
	{
		'type': 'local',
		'command': '###COPY COMMAND### ###FULL HOSTNAME###:/tmp/aptdate-###HOSTNAME###.tmp ' + var_dir, #+ " >/dev/null",
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
		'type': 'local',
		'command': "scp /root/programs-base-20110117.tar.bz2 ###FULL HOSTNAME###:",
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "rm -rf /tmp/programs",
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "tar xf /home/###USERNAME###/programs-base-20110117.tar.bz2 -C /tmp",
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "mkdir -p /root/tools",
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "cp -a /tmp/programs/* /root/tools/",
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "rm -rf /tmp/programs",
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "echo '0  5    * * *   root    /root/tools/bin/aptdate.sh' >> /etc/crontab",
	},
	{
		'command key': 'continue',
		'expect': server['root prompt'],
		'command': "/root/tools/bin/aptdate.sh &",
	},
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
