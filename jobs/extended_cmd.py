### example job file

import sys
import time

task = 'Testing task'
logfile = open(log_dir + '/cmd-' + time.strftime("%Y-%m-%d") + '.log','a')
# logfile = sys.stdout

#cmd = sys.argv[3]

cmds = [
	{
		'expect': server['prompt'],
		'command': "sed 's/^HOSTNAME\=.*$/HOSTNAME=" + server['hostname'] + "/' /etc/sysconfig/network > /root/network",
	},
	{
		'expect': server['prompt'],
		'command': "rm -f /etc/sysconfig/network",
	},
	{
		'expect': server['prompt'],
		'command': "mv /root/network /etc/sysconfig/network",
	},
	{
		'expect': server['prompt'],
		'command': "cat /etc/sysconfig/network",
	},
]

