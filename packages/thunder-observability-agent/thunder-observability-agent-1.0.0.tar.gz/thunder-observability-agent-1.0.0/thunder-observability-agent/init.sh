#!/bin/bash
# A10 TOA configuration script, using bash
#
# Bash tutorial: http://linuxconfig.org/Bash_scripting_Tutorial#8-2-read-file-into-bash-array
# My scripting link: https://github.com/a10networks/thunder-observability-agent
#
# Usage: ./init.sh file
# # exit 9999 # die with error code 9999
# 
# --------------------------------------------------------

### Create virtual environment ###
### virtualenv toaenv
### source toaenv/bin/activate
### echo "Successfully created python virtual environment with name 'toaenv'."

### Install plugin dependencies ###
pip3 install requests>=2.27.1
pip3 install boto3>=1.23.10
echo "Successfully installed TOA dependencies."

### Set default toa config directory ###
export TOA_CONFIG_PATH="/usr/toaenv/thunder-observability-agent"
echo "TOA configuration files directory: /usr/toaenv/thunder-observability-agent"
echo "TOA_CONFIG_PATH : "$TOA_CONFIG_PATH


### Set default toa config directory ###
export PATH="/usr/toaenv/lib/python3/site-packages/thunder-observability-agent:$PATH"
echo "TOA plugin directory: /usr/toaenv/lib/python3/site-packages/thunder-observability-agent"
echo "PATH : "$PATH


### Set crontab schedule ###
crontab -l | { cat; echo '*/1 * * * * /usr/toaenv/bin/python3 /usr/toaenv/lib/python3.10/site-packages/thunder-observability-agent/toa.py'; } | crontab -
echo "Crontab frequency set : */1 * * * * /usr/toaenv/bin/python3 /usr/toaenv/lib/python3.10/site-packages/thunder-observability-agent/toa.py"
# service rsyslog start
# service cron start


### Check if a directory does not exist ###
echo "Secrets config directory: /root/" 
if [ ! -d "/root/.aws" ]
then
    ### echo "Directory /root/.aws DOES NOT exists." 
	cp -r .tmp/config/.aws /root/.aws
fi

if [ ! -d "/root/.azure" ]
then
    ### echo "Directory /root/.azure DOES NOT exists." 
	cp -r .tmp/config/.azure /root/.azure
fi

if [ ! -d "/root/.vmware" ]
then
    ### echo "Directory /root/.vmware DOES NOT exists." 
	cp -r .tmp/config/.vmware /root/.vmware
fi

if [ ! -d "/root/.thunder" ]
then
    ### echo "Directory /root/.thunder DOES NOT exists." 
	cp -r .tmp/config/.thunder /root/.thunder
fi

if [ ! -d "/var/log/thunder-observability-agent" ]
then
	mkdir /var/log/thunder-observability-agent
	echo "Log directory: var/log/thunder-observability-agent" 
fi