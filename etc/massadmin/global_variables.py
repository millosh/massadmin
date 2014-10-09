### example global variables file

global_variables = [
	{
		'argument id': 'username',
		'type': 'input',
		'replaces': [ "servers exec", "job exec", ],
		'text': 'Username: ',
		'key': '###USERNAME###',
	},
	{       
		'argument id': 'sudo password',
		'type': 'getpass',
		'replaces': [ "job exec", ],
		'text': 'Password: ',
		'key': '###PASSWORD###',
	},      
]

