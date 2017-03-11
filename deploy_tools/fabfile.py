from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/SpaIns/CSS498-Django.git'

#Command I used to run this:
#fab deploy:host=steffan@192.168.1.17 --port=56734 -i /home/spa/Desktop/id_rsa


def deploy():
    #the second argument should be env.host in reality
    site_folder = '/home/%s/sites/%s' %(env.user, 'superlists-staging.django498.ga')
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))
    #The static folder is actually in the source folder
    run('mkdir -p %s/%s' % (site_folder + '/source', 'static'))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        #Had to change this up a bit; since static is being made in
        #The 'source' folder first, it won't allow for a clone.
        #So instead, I'll manually init, add an origin, and pull from it
        run('cd %s && git init && git remote add origin %s && git pull origin master' % (source_folder,REPO_URL))
        #run('git init')
        #run('git remote add origin %s' % (REPO_URL,))
        #run('git pull origin master')
    current_commit = local("git log -n 1 --format=%H", capture=True) #getting an error here, not sure why...
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    #may have to add the website address manually here
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s", "%s", "%s"]' % (site_name, "django498.ga", "http://django498.ga",) #just added last 2 w/o testing
    )
    secret_key_file = source_folder + '/superlists/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('python3 -m venv %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))

def _update_static_files(source_folder):
    run('cd %s && ../../virtualenv/bin/python manage.py collectstatic --noinput' % (source_folder + '/superlists',))

    #last thing thats broken is this;
    #'unable to open database file'
    #I'm going to need to add another .. for the database
    #it's currently '../database/db.sqlite3'
    #should be '../../database/db.sqlite3'
    #do a sed I assume
def _update_database(source_folder):
    settings_path =  source_folder + '/superlists/superlists/settings.py'
    sed(settings_path, "../database/db.sqlite3", "../../database/db.sqlite3")
    run('cd %s && ../../virtualenv/bin/python manage.py migrate --noinput' % (source_folder + '/superlists',))