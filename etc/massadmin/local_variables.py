### example local variables file

if 'remote' in server: 
	if server['remote'] == 'yes':
		access_command = 'ssh' 
		copy_command = 'scp' 
	else:   
		access_command = '###SKIP###'
		copy_command = '###SKIP###'
else:   
	access_command = 'ssh'
	copy_command = 'scp' 

local_variables = [
	{
		'argument id': 'hostname',
		'type': 'replace',
		'replaces': [ "job exec", ],
		'key': '###HOSTNAME###',
		'value': server['hostname'],
	},
	{
		'argument id': 'full hostname',
		'type': 'replace',
		'replaces': [ "job exec", ],
		'key': '###FULL HOSTNAME###',
		'value': server['full hostname'],
	},
	{
		'argument id': 'copy command',
		'type': 'replace',
		'replaces': [ "job exec", ],
		'key': '###COPY COMMAND###',
		'value': copy_command,
	},
	{
		'argument id': 'access command',
		'type': 'replace',
		'replaces': [ "job exec", ],
		'key': '###ACCESS COMMAND###',
		'value': access_command,
	},
]

