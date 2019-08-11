from fabric import task, Connection
from invoke import ta
import random

REPO_URL = 'https://github.com/simbas2000/DjangoTest1.git'


def _create_directory_structure_if_necessary(c: Connection, site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        c.run('mkdir -p {}/{}'.format(site_folder, subfolder))


def _get_latest_source(c: Connection, source_folder):
    result = c.run('test -a {}/.git && echo 1 || echo 0'.format(source_folder))
    if result.stdout.strip() == "1":
        run


@task
def deploy(c):
    site_folder = '/home/%s/sites/%s' % (c.user, c.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, c.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
