"""

how to run:  fab -H demo.loc --user vagrant --password vagrant --set=domain=demo.loc,ip=192.168.33.111 setup

"""
from fabric.api import *
import fabtools
from unipath import Path
from fabric.colors import red
from ffw import *

env.project = 'drupal'
env.version = '8.2.5'

env.ssh = '/home/%s/.ssh' % env.user
env.home = Path('/', 'home', env.user)
env.project_dir = Path(env.home, env.project)
env.site_username = 'admin'
env.site_password = 'admin'
env.drush_path = Path(env.home, '.config/composer/vendor/drush/drush/drush')

env.db = {
    'host': 'localhost',
    'name': env.project,
    'user': env.user,
    'pass': genpass(),
    'port': 3306,
    'root': 'MBiotHo3ZdIP9yp1',
    'type': 'mysql',
    'driver': 'pdo_mysql',
    'site_username': env.site_username,
    'site_password': env.site_password,
    'drush_path': env.drush_path,
    'project_dir': env.project_dir
}


def install_pgsql():
    fabtools.require.postgres.server()
    fabtools.require.postgres.user(env.db['user'], env.db['pass'])
    fabtools.require.postgres.database(env.db['name'], owner=env.db['user'])
    fabtools.require.service.started('postgresql')


def install_project_drush():
    run("mkdir -p %s" % env.project_dir)
    run("curl -sS https://getcomposer.org/installer | php")
    sudo("mv composer.phar /usr/local/bin/composer") 
    run("composer global init -n")
    run("composer global update")
    run("composer global require drush/drush:8.*")
    with cd(env.project_dir):
        run("/home/vagrant/.config/composer/vendor/drush/drush/drush dl drupal-8.2.5")
        run("mv drupal-8.2.5/* {}".format(env.project_dir))
        run("rm -r drupal-8.2.5")
        command = '/home/vagrant/.config/composer/vendor/drush/drush/drush site-install standard --account-name={site_username} \
        --account-pass={site_password} --db-url={type}://{user}:{pass}@127.0.0.1:{port}/{name} -y'.format(**env.db)
        run(command)
        run("chmod -R 0777 %s/sites/default/files" % env.project_dir)
    source = Path('apache', '.htaccess')
    put('apache/.htaccess', remote_path="{}".format(env.project_dir))


def drush_help():
    with cd(env.project_dir):
        run('%s help' % env.drush_path)

def drush_status():
    with cd(env.project_dir):
        run('%s status' % env.drush_path)

def clear_cache():
    with cd(env.project_dir):
        run('%s cc' % env.drush_path)


def config_apache():
    with open('./apache/site.conf') as fn:
        config_tpl = fn.read()
    fabtools.require.apache.site(
        env.domain,
        template_contents=config_tpl,
        port=80,
        domain=env.domain,
        docroot=env.project_dir
    )


def report():
    run("clear")
    print (red("-----------------------------------"))
    print(red("Congratulations, Drupal has been successfully installed, visit http://%s") % env.domain)
    print(red("login - {}".format(env.site_username)))
    print(red("password - {}".format(env.site_password)))


def setup():
    sudo("add-apt-repository -y ppa:ondrej/php")
    #sudo("apt-get update && apt-get -y dist-upgrade")
    sudo("apt-get update")
    fabtools.require.apache.server()
    sudo("a2enmod rewrite")
    fabtools.require.deb.packages(
        ['php7.0', "php7.0-gd", "php7.0-sqlite", "php7.0-curl",
         "php7.0-xml", "php7.0-mbstring", "git", "unzip"]
    )
    if env.db['driver'] == "pdo_mysql":
        fabtools.require.deb.package("php7.0-mysql")
        install_mysql()
    else:
        fabtools.require.deb.package("php7.0-pgsql")
        env.db['type'] = 'pgsql'
        env.db['port'] = 5432
        install_pgsql()
    install_project_drush()
    config_apache()
    report()

