from fabric.api import env, run

#I think I need to include stuff from the past fabfile re: host auth with rsa key etc

def _get_base_folder(host):
	return '~/sites/' + host

def _get_manage_dot_py(host):
	return '{path}/virtualenv/bin/python {path}/source/superlists/manage.py'.format(
		path=_get_base_folder(host)
	)

def reset_database():
	run('{manage_py} flush --noinput'.format(
		manage_py=_get_manage_dot_py(env.host)
	))

def create_session_on_server(email):
	session_key = run('{manage_py} create_session {email}'.format(
		manage_py=_get_manage_dot_py(env.host),
		email=email,
	))
	print(session_key)