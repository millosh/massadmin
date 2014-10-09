#!/usr/bin/python
# -*- coding: utf-8 -*-

# Goals:
# 0.0.1: exec commands, send files, recieve files
# 0.0.2: generalization: ###PROMPT###, separate server conf, catagorizations of servers
# 0.1.0: different variables per server; conditional according to server config
# 0.2.0: taking output

import re
import os, sys
import pexpect
import getpass

root_dir = "/home/millosh/rad/software/massadmin/dev"
bin_dir = root_dir + "/bin"
etc_dir = root_dir + "/etc/massadmin"
var_dir = root_dir + "/var"
job_dir = etc_dir + "/jobs"
log_dir = var_dir + "/logs"
global_variables_file = etc_dir + "/global_variables.py"
local_variables_file = etc_dir + "/local_variables.py"
servers_file = etc_dir + "/servers.py"

fd = sys.argv[1]

def process_job(cmd,child,command_key):
	if 'type' in cmd:
		if cmd['type'] == 'start':
			child = pexpect.spawn(cmd['command'])
			child.logfile = logfile
		elif cmd['type'] == 'local':
			os.system(cmd['command'])
		elif cmd['type'] == 'conditional function':
			result = cmd['condition']['function']()
			values = cmd['condition']['values'][result]
			if values['type'] == 'string':
				if values['command'] == 'print':
					print "iz printa", values['string']
				else:
					values['command'](values['string'])
			elif values['type'] == 'command key':
				command_key = values['command key']
	else:
		child.expect("(" + cmd['expect'] + ")")
		if 'optional' in cmd:
			group = child.match.groups()[0]
			if cmd['optional']['type'] == 'simple':
				if group == cmd['optional']['condition']:
					command = cmd['command']
				else:
					command = ''
		else:
			command = cmd['command']
		child.sendline(command)
	print 'CMD:', cmd['command']
	return child, command_key

servers_exec = open(servers_file).read()
job_exec = open(fd).read()
global_variables_exec = open(global_variables_file).read()
local_variables_exec = open(local_variables_file).read()
child = ''

exec(global_variables_exec)

for gvar in global_variables:
	if gvar['type'] == 'input':
		key = gvar['key']
		value = raw_input(gvar['text'])
	elif gvar['type'] == 'getpass':
		key = gvar['key']
		value = getpass.getpass(gvar['text'])
	elif gvar['type'] == 'replace':
		key = gvar['key']
		value = gvar['value']
	for grep in gvar['replaces']:
		if grep == "servers exec":
			servers_exec = re.sub(key,value,servers_exec)
		elif grep == "job exec":
			job_exec = re.sub(key,value,job_exec)

exec(servers_exec)

for server in servers:
	command_key = ''
	print 'SERVER: ' + server['server id']
	exec(local_variables_exec)
	job_exec_tmp = job_exec
	for lvar in local_variables:
		if lvar['type'] == 'replace':
			for lrep in lvar['replaces']:
				if lrep == "job exec":
					job_exec_tmp = re.sub(lvar['key'],lvar['value'],job_exec_tmp)
	exec(job_exec_tmp)
	for cmd in cmds:
		if command_key != '':
			if 'command key' in cmd:
				if re.search(cmd['command key'],command_key):
					child, command_key = process_job(cmd,child,command_key)
				else:
					pass
			else:
				pass
		else:
			if '###SKIP###' in cmd['command']:
				pass
			else:
				child, command_key = process_job(cmd,child,command_key)

