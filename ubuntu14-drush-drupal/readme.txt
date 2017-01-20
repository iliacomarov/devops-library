This script make clean installation of LAMP(php + apache + mysql/postgresql) + drush + drupal on the vagrant-machine with Ubuntu 14.04

Steps:
1. add to your /etc/hosts next line
demo.loc 192.168.33.111 

2. run locally: 
chmod u+x ./preinstall.sh && sh ./preinstall.sh

3. check and configure fabfile/__init__.py and then run locally: 
fab -H demo.loc --user vagrant --password vagrant --set=domain=demo.loc,ip=192.168.33.111 setup
