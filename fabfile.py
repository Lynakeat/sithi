#
# Required Files to be in /conf:
# <project_name>.wsgi,
# <project_name>_staging_apache.conf,
# <project_name>_deployment_apache.conf,
# staging_settings.py,
# production_settings.py,
# and requirements.txt (for virtualenv install)
#
# Any elements you want installed in the virutalenv during setup should be
# added to requirements.txt

# TODO's / Random Ideas
#
# - Production setup
# - Make database setup more intelligent (choose setup based on database
#   type in __settings__, etc)
# - Turn asset_path into list so we can loop through it on setup/deploy to
#   get all "asset" paths included
# - Refactor the whole thing, since there's a lot of repeated code

from datetime import datetime

from fabric.api import *
from fabric.contrib.console import confirm

#
#    Project Configuration
#
env.project_name = 'activebuys'
env.site_name = 'activebuys'
env.domain = 'activebuys.com'
env.production_ftp_username = 'serveradmin'

# Shared Variables (usually do not need editing)
env.staging_hosts = ['198.101.197.233', ]
env.production_hosts = ['198.101.197.233', ]
env.repo_url = 'git@github.com:ACTIVEBUYS/%(project_name)s.git' % env
env.branch = 'master'

# Virtualenv
env.virtualenv_workon_path = '/apps/.virtualenvs'

#
#    Modes
#
def staging():
    """Sets Fabric to staging server mode
    """
    env.virtualenv_name = 'activebuys-staging-env'
    env.virtualenv_path = '%(virtualenv_workon_path)s/%(virtualenv_name)s' % env
    env.activate_virtualenv = 'source %(virtualenv_path)s/bin/activate;' % env

    env.app_path = '/apps/%(project_name)s-staging' % env
    env.hosts = env.staging_hosts
    env.webroot = '/var/www/%(project_name)s-staging' % env
    env.shared_user = 'www-data'
    env.asset_path = '%(webroot)s/static/assets' % env
    
    env.shared_path = '%(app_path)s/shared' % env
    env.releases_path = '%(app_path)s/releases' % env
    env.current_path = '%(app_path)s/current' % env
    env.database_path = '%(shared_path)s/%(project_name)s.db' % env
    env.settings_path = '%(current_path)s/%(project_name)s/sites/%(site_name)s/conf/settings' % env
    env.settings_file = '%(settings_path)s/staging_settings.py' % env
    env.manage = '%(current_path)s/%(project_name)s/manage.py' % env
    env.dumpfile = '%(shared_path)s/dump.json' % env
    

def production():
    """Sets Fabric to production server mode
    """
    env.virtualenv_name = 'activebuys-env'
    env.virtualenv_path = '%(virtualenv_workon_path)s/%(virtualenv_name)s' % env
    env.activate_virtualenv = 'source %(virtualenv_path)s/bin/activate;' % env

    env.app_path = '/apps/%(project_name)s' % env
    env.hosts = env.production_hosts
    env.webroot = '/var/www/%(project_name)s' % env
    env.shared_user = 'www-data'
    env.asset_path = '%(webroot)s/static/assets' % env

    env.shared_path = '%(app_path)s/shared' % env
    env.releases_path = '%(app_path)s/releases' % env
    env.current_path = '%(app_path)s/current' % env
    env.database_path = '%(shared_path)s/%(project_name)s.db' % env
    env.settings_path = '%(current_path)s/%(project_name)s/sites/%(site_name)s/conf/settings' % env
    env.settings_file = '%(settings_path)s/production_settings.py' % env
    env.activate_virtualenv = 'source %(shared_path)s/%(virtualenv_name)s/bin/activate;' % env
    env.manage = '%(current_path)s/%(project_name)s/manage.py' % env
    env.dumpfile = '%(shared_path)s/dump.json' % env

#
#    Actions
#
def setup():
    """Setup project and site environments on server indicated
    """
    require('hosts', provided_by = [staging, production])

    project_setup()

    if env.hosts == env.staging_hosts:
        _staging_conf()
        _staging_assets()
    elif env.hosts == env.production_hosts:
        if confirm("Has the domain been created on RainCloud?"):
            _production_conf()
            _production_assets()
    else:
        print "-- No site setup function for this host --"

########## Staging Site Setup ##########
@hosts('staging.activebuys.com')
def staging_site_setup(*args):
    """Setup site information on staging
        usage: fab staging_site_setup:site1,site2,site3
    """

    if args:
        for arg in args:
            env.site_name = arg
            _staging_conf()
    else:
        print "-- No sites specified.\n\nUsage:\nfab staging_site_setup:site1,site2,site3"

def _staging_conf():
    print "-- Staging Site Setup for %(site_name)s --" % env

    ### Apache ###
    print "\n-- Configuring Apache for %(site_name)s --" % env
    # Create conf in sites-available
    env.conf = "/foo/apache/sites-available/%(site_name)s" % env
    sudo("touch %(conf)s" % env)
    sudo("chown %(user)s:staff %(conf)s" % env)
    put("sites/%(site_name)s/conf/conf/%(site_name)s_apache.conf" % env, "%(conf)s" % env)

    # Create symlink in sites-enabled and step number by +1 correctly
    env.last = int(run("ls -C1 /foo/apache/sites-enabled | tail -1 | sed 's/\\([0-9]*\\).*/\\1/'"))
    env.next = str(1 + env.last)
    while len(env.next) < 3:
        env.next = '0%(next)s' % env
    sudo("ln -s %(conf)s /foo/apache/sites-enabled/%(next)s-%(site_name)s" % env)

def _staging_assets():
    print "\n-- Configuring Local Media Path --" % env
    # Create assets directory
    sudo("mkdir -p %(asset_path)s" % env)
    sudo("chown -R www-data:staff %(webroot)s" % env)

########## Production Site Setup ##########
@hosts('raincloud-01')
def production_site_setup():
    """Setup site information on RainCloud
        usage: fab production_site_setup:site1,site2,site3
    """

    if args:
        for arg in args:
            _production_conf()
    else:
        print "-- No sites specified.\n\nUsage:\nfab staging_site_setup:site1,site2,site3"

def _production_conf():
    print "-- Production Site Setup for %(site_name)s --" % env

    ### Apache ###
    print "\n-- Configuring Apache for %(site_name)s --" % env
    # Create conf in sites-available
    env.conf = "/foo/apache/sites-available/%(site_name)s" % env
    sudo("touch %(conf)s" % env)
    sudo("chown %(user)s:staff %(conf)s" % env)
    put("sites/%(site_name)s/conf/conf/%(site_name)s_apache.conf" % env, "%(conf)s" % env)

    # Create symlink in sites-enabled and step number by +1 correctly
    env.last = int(run("ls -C1 /foo/apache/sites-enabled | tail -1 | sed 's/\\([0-9]*\\).*/\\1/'"))
    env.next = str(1 + env.last)
    while len(env.next) < 3:
        env.next = '0%(next)s' % env
    sudo("ln -s %(conf)s /foo/apache/sites-enabled/%(next)s-%(site_name)s" % env)

def _production_assets():
    print "\n-- Configuring Local Media Path --"
    # Create assets directory
    sudo("mkdir -p %(asset_path)s" % env)
    sudo("chmod 775 %(asset_path)s" % env)

########## Shared Setup Methods ##########
def project_setup():
    """Create the project environment"""
    print "\n-- Setting up the project environment --"
    # Initiate shared path
    sudo("mkdir -p %(shared_path)s %(releases_path)s" % env)

    # Temporary permissions for creating virtualenv
    sudo("chmod -R g+w %(app_path)s" % env)
    sudo("chown -R deploy:%(shared_user)s %(app_path)s" % env)

    _create_virtualenv()

    # Reset permissions
    print "\n-- Resetting Permissions --"
    sudo("chmod -R g+w %(app_path)s" % env)
    sudo("chown -R deploy:deploy %(app_path)s" % env)
    sudo("chown -R deploy:%(shared_user)s %(shared_path)s" % env)

def _create_virtualenv():
    """Create virtualenv and install requirements via pip"""
    print "\n-- Configuring Virtualenv --"
    put('requirements.txt' % env, '%(shared_path)s/requirements.txt' % env)
    run('cd %(shared_path)s/; virtualenv %(virtualenv_name)s' % env)

    print "\n-- Installing Dependencies --"
    sudo('cd %(shared_path)s/; pip install -E %(virtualenv_name)s -r %(shared_path)s/requirements.txt' % env)

########## Other Actions ##########
def deploy(branch=None):
    """Deploy current version from repository to selected server

    Optionally, deploy from a specific branch.
    """
    if branch:
        env.branch = branch
    require('hosts', provided_by = [staging, production])
    if env.hosts == env.staging_hosts:
        local("git tag -f Staging")
    elif env.hosts == env.production_hosts:
        local("git tag -f Production")
    env.user = 'deploy'
    env.datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    env.release_path = '%(releases_path)s/%(datetime)s' % env
    run("mkdir -p %(release_path)s" % env)
    run("git clone --branch %(branch)s --depth 1 %(repo_url)s %(release_path)s/%(project_name)s" % env)
    run("ln -s %(asset_path)s %(release_path)s/%(project_name)s/media" % env)
    run("if [ -e %(current_path)s ]; then rm %(current_path)s; fi" % env)
    run("ln -s %(release_path)s %(current_path)s" % env)
    run("ln -s %(settings_file)s %(current_path)s/%(project_name)s/local_settings.py" % env)

def deploy_static():
    require('hosts', provided_by = [staging, production])
    env.user = 'deploy'
    run('%(activate_virtualenv)s python %(manage)s collectstatic -v0 --noinput' % env)

def restart():
    """Restarts Apache, thus restarting updated django projects
    """
    require('hosts', provided_by = [staging, production])
    env.user = 'deploy'
    run("sudo /etc/init.d/apache2 restart")

# def install_requirements():
#     """Perform `pip install -r requirements.txt` """
#     # requires user with 'sudo' privileges
#     run('%(activate_virtualenv)s' % env)
#     sudo('cd %(current_path)s/%(project_name)s; pip install -r requirements.txt' % env)

# def syncdb():
#     """Perform `python manage.py syncdb` (Not recommended since it doesnt function properly thru fab)"""
#     # requires user with 'sudo' privileges
#     run('%(activate_virtualenv)s python %(manage)s syncdb' % env)

# def migrate():
#     """Perform `python manage.py migrate` (South)"""
#     # requires user with 'sudo' privileges
#     run('%(activate_virtualenv)s python %(manage)s migrate' % env)

# def dumpdata(*apps):
#     """Perform python manage.py dumpdata"""
#     env.appstring = ''
#     for app in apps:
#         env.appstring += u'%s ' % app
#     env.appstring = env.appstring[:-1]
#     run('%(activate_virtualenv)s python %(manage)s dumpdata %(appstring)s --indent=2 > %(dumpfile)s' % env)

# def loaddata():
#     """Reloads the dump fixture"""
#     run('%(activate_virtualenv)s python %(manage)s loaddata %(dumpfile)s' % env)

def errorlog():
    """`tail -f` the error log for today"""
    if env.hosts == env.staging_hosts:
        now = datetime.now()
        infodict = {
            'project_name': env.project_name,
            'Y': now.year,
            'm': int(now.month),
            'd': int(now.day),
        }
        run("tail -f /foo/apache/log/sites/%(project_name)s/%(Y)s/%(Y)s-%(m)02d-%(d)02d-errors.log" % infodict)
    elif env.hosts == env.production_hosts:
        run("tail -f /var/www/vhosts/%(domain)s/statistics/logs/error_log" % env)
    else:
        print "-- No log function for this host --"
