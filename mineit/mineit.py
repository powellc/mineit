"""MineIt.

Usage:
    mineit create <servername> [--port=<port>] [--memory=<memory>] [--motd=<motd>] [--version=<version>]
    mineit set <servername> <option> <value>
    mineit delete <servername>
    mineit list
"""

import os
from pwd import getpwnam
from grp import getgrnam
from shutil import copy, rmtree
from docopt import docopt


LATEST_RELEASE = '1.7.9'
BASE_DIR = '/home/minecraft/'
SUPERVISOR_DIR = '/etc/supervisor/conf.d/'
RELEASES_DIR = os.path.join(BASE_DIR, 'releases')
MAX_MEMORY = '1024M'
SCONF = ("[program:{0}]\n"
         "command=java -Xmx{1} -Xms1024M -jar /home/minecraft/{2}/minecraft_server.{3}.jar nogui\n"
         "directory=/home/minecraft/{4}/\n"
         "user=minecraft\n"
         "autostart=true\n"
         "autorestart=true\n"
         "stdout_logfile=/home/minecraft/{5}/logs/supervisor.log\n"
         "stopsignal=QUIT\n")


def main(args=None):
    """Here we hand off for the various cli functions"""
    if not args:
        args = docopt(__doc__, version="xxxx")
    if args['create']:
        create_server(args['<servername>'], port=args['--port'])
    if args['delete']:
        delete_server(args['<servername>'])



if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)


def create_server(name, port=None, memory=None, motd=None, version=None):
    """
    Create a new minecraft server.

    3. Create supervisor config file

    """
    if not memory:
        memory = MAX_MEMORY

    # First we create a new folder in the minecraft base dir
    folder = os.path.join(BASE_DIR, name)
    if not os.path.exists(folder):
        os.system('sudo -u minecraft mkdir {0}'.format(folder))

    # Second, we copy our jar file into the new folder
    jar_file = RELEASES_DIR + '/minecraft_server.{0}.jar'.format(LATEST_RELEASE)
    try:
        os.system('sudo -u minecraft cp {0} {1}'.format(
            jar_file, os.path.join(folder)))
    except:
        delete_server(name)

    # Finally, we create a supervisor config file
    try:
        f = open(os.path.join(SUPERVISOR_DIR, name + '.conf'), 'w')
        try:
            f.write(SCONF.format(name, memory, name, LATEST_RELEASE, name, name))
        finally:
            f.close()
    except IOError:
        delete_server(name)
    try:
        os.system('sudo -u minecraft mkdir {0}'.format(folder + '/logs'))
        os.system('sudo -u minecraft touch {0}/supervisor.log'.format(folder + '/logs'))
    except IOError:
        pass
    os.system('supervisorctl update')

    if port:
        os.system('sudo -u minecraft sed -e "s/^server-port=/server-port={0}/g" {1}'.format(
            port, folder + '/server.properites'))

    os.system('supervisorctl restart {0}'.format(name))


def set_config(name, option, value):
    pass

def delete_server(name):
    # First we create a new folder in the minecraft base dir
    folder = os.path.join(BASE_DIR, name)
    if os.path.exists(folder):
        try:
            rmtree(folder)
        except:
            pass
    try:
        os.remove(os.path.join(SUPERVISOR_DIR, name + '.conf'))
    except:
        pass
    os.system('supervisorctl reread')
