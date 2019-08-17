from fabric import task, Connection
from invoke import run as local_run
import shutil
import os
import re
import random

REPO_URL = 'https://github.com/simbas2000/DjangoTest1.git'


def _exists(c: Connection, path):
    result = c.run('test -a {} && echo 1 || echo 0'.format(path))
    return result.stdout.strip() == "1"


def _create_directory_structure_if_necessary(c: Connection, site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        c.run('mkdir -p {}/{}'.format(site_folder, subfolder))


def _get_latest_source(c: Connection, source_folder):
    if _exists(c, '{}/.git'.format(source_folder)):
        c.run('cd {} && git fetch'.format(source_folder))
    else:
        c.run('git clone {} {}'.format(REPO_URL, source_folder))
    current_commit = local_run('git log -n 1 --format=%H')  # LAUNCH FAB FROM LOCAL REPO DIR AFTER PUSH
    c.run('cd {} && git reset --hard {}'.format(source_folder, current_commit.stdout.strip()))


def _update_settings(c: Connection, source_folder, sitename):
    settings_path = source_folder + '/superlists/settings.py'
    secret_key_path = source_folder + '/superlists/secret_key.py'
    loc_tmp_dir = 'tmp_remote_settings'
    loc_new_settings_path = loc_tmp_dir + '/settings.py'
    loc_old_settings_path = loc_tmp_dir + '/settings_old.py'
    loc_secret_key_path = loc_tmp_dir + '/secret_key.py'
    os.mkdir(loc_tmp_dir)
    try:
        c.get(settings_path, local=os.getcwd()+'/'+loc_tmp_dir+'/settings.py')
        os.rename(loc_tmp_dir+'/settings.py', loc_old_settings_path)
        with open(loc_old_settings_path, 'r') as f:
            content = f.read()
            new_content = re.sub("DEBUG = True", "DEBUG = False", content)
            new_content = re.sub(r'ALLOWED_HOSTS = \[.*\]', 'ALLOWED_HOSTS = ["{}"]'.format(sitename), new_content)
            new_content = re.sub(r"SECRET_KEY = '.*'", 'from .secret_key import SECRET_KEY', new_content)
            with open(loc_new_settings_path, 'w') as nf:
                nf.write(new_content)
            if not _exists(c, secret_key_path):
                chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
                key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
                with open(loc_secret_key_path, 'w') as nkey:
                    nkey.write('SECRET_KEY = "{}"'.format(key))
                c.put(os.getcwd()+'/'+loc_secret_key_path, remote=source_folder+'/superlists/')
            c.put(os.getcwd()+'/'+loc_new_settings_path, remote=source_folder+'/superlists/')
    finally:
        shutil.rmtree(loc_tmp_dir)


def _update_virtualenv(c: Connection, source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not _exists(c, virtualenv_folder + '/bin/pip'):
        c.run('virtualenv --python=python3 {}'.format(virtualenv_folder))
    c.run('{}/bin/pip install -r {}/requirements.txt'.format(virtualenv_folder, source_folder))


def _update_static_files(c: Connection, source_folder):
    c.run('cd {} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(source_folder))


def _update_database(c: Connection, source_folder):
    c.run('cd {} && ../virtualenv/bin/python3 manage.py migrate --noinput'.format(source_folder))


@task
def deploy(c):
    site_folder = '/home/%s/sites/%s' % (c.user, c.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(c, site_folder)
    _get_latest_source(c, source_folder)
    _update_settings(c, source_folder, c.host)
    _update_virtualenv(c, source_folder)
    _update_static_files(c, source_folder)
    _update_database(c, source_folder)
