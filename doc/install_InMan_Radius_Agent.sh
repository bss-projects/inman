#!/bin/bash

INMAN_DEST_MAIN_PATH="/opt/inman"
INMAN_DEST_AGENT_PATH="$INMAN_DEST_MAIN_PATH/agent_freeradius"

group="inman"
login="im_cluster_sync"
shell="/bin/bash"
base_dir="/home"
home_usr_dir="$base_dir/$login"

yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E '%{rhel}').noarch.rpm
yum -y update
yum -y install mlocate
yum -y install openssh
yum -y install openssh-server
yum -y install nano
yum -y install less
yum -y install gcc
yum -y install gcc-c++
yum -y install make 
yum -y install zlib-devel
yum -y install wget
yum -y install automake
yum -y install autoconf
yum -y install libtool
yum -y install sudo
yum -y install python
yum -y install python-devel
yum -y install python-pip
yum -y install redis
systemctl enable redis
systemctl start redis

###
# Dependencies for asciimatics->Pillow just in case
###
#yum -y install libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libharfbuzz-dev libfribidi-dev tcl8.6-dev tk8.6-dev python-tk
#yum -y install jpeg-dev
#yum -y install libwebp-devel
#yum -y install libjpeg-devel

pip install --upgrade pip
pip install setuptools_scm
pip install asciimatics
pip install configobj
pip install jinja2
pip install setproctitle
pip install redis
pip install autobahn
pip install twisted
pip install service_identity
pip install x509
pip install nuitka

cd install_inman_radius_agent

mkdir -p $INMAN_DEST_AGENT_PATH
mkdir -p /var/run/im/

###
# Create user to share data with an other cluster node to avoid root
###
echo "Create group: $group"
groupadd $group

echo "Create user:"
echo -e " User: $login\n Group: $group"
useradd -g $group -b $base_dir -d $home_usr_dir -m -s $shell $login
mkdir -p /home/$login/.ssh && chown $login:$group /home/$login/.ssh
echo -e "tgbyhnuj\ntgbyhnuj" | passwd $login
passwd -x 1 $login
echo "im_cluster_sync ALL=NOPASSWD:/bin/passwd -d $login, /usr/bin/chage -m 0 -M 99999 -I -1 -E -1 $login" >> /etc/sudoers
echo -e "#"'!'"/bin/bash\nsudo /bin/passwd -d $login\nsudo /usr/bin/chage -m 0 -M 99999 -I -1 -E -1 $login\nrm -f /home/$login/null_password.sh" > /home/$login/null_password.sh
chown $login:$group /home/$login/null_password.sh
chmod 700 /home/$login/null_password.sh

echo "if [ \"\$SSH_TTY\" ]; then /home/\$LOGNAME/null_password.sh; fi" >> /home/$login/.bashrc


###
# Compile and install Agent
###
cd im_freeradius # Go into agent source directory

nuitka --recurse-to=im_clientfileconfigclass_freeradius --recurse-to=im_agentconfigclass_freeradius im_agentside_freeradius.py
nuitka --recurse-to=im_agentconfigclass_freeradius im_agentside_websocket_freeradius.py

cp im_agentside_freeradius.exe im_agentside_websocket_freeradius.exe agent_stop_daemon_freeradius.sh im_agent_freeradius_confcheck.cfg $INMAN_DEST_AGENT_PATH

cp logrotate_freeradius /etc/logrotate.d/
cp logrotate_freeradius_log /etc/logrotate.d/
cp logrotate_im_freeradius /etc/logrotate.d/
cp rlm_im_freeradius.py /usr/lib/python2.7/site-packages

cp im_agent_freeradius.service /usr/lib/systemd/system/
cp im_agent_websocket_freeradius.service /usr/lib/systemd/system/

###
# Insert Agent conf element in Freeradius
###

cp radius_mod_python_conf /etc/freeradius/mods-available/python

###
# Calling Python TUI to create configuration file for IM Agent
###
python python_tui_conf_agent_freeradius.py "$INMAN_DEST_AGENT_PATH"

cd /etc/freeradius/mods-enabled
ln -s ../mods-available/python python

touch /etc/freeradius/clients_im_range.conf /etc/freeradius/clients_im.conf
sed -i '/$INCLUDE clients.conf/a $INCLUDE clients_im.conf' /etc/freeradius/radiusd.conf
sed -i '/$INCLUDE clients_im.conf/a $INCLUDE clients_im_range.conf' /etc/freeradius/radiusd.conf

sed -i 's/auth = no/auth = yes/' /etc/freeradius/radiusd.conf # Log AUTH action on RADIUS

# Insert declaration in RADIUS conf to use RLM python mod for authorize and authenticate part 
line_count=0
flag=0
flag_detect_begin_brace=0

while read p; do
	line_count=$((line_count+1))
	if [[ $p =~ ^authorize ]]; then
		flag=1
	fi
  
	if [ $flag = 1 ]; then

		if [[ $p =~ "{" ]]; then
			flag_detect_begin_brace=1
		fi

		if [[ $p =~ "}" && $flag_detect_begin_brace == 0 ]]; then
			sed -i "$line_count i\\\tpython" /etc/freeradius/sites-enabled/default
			flag=0
		elif [[ $p =~ "}" ]]; then
			flag_detect_begin_brace=0
		fi
	fi

done </etc/freeradius/sites-enabled/default

sed -i '/authenticate {/a \\tAuth-Type Python {\n\t\tpython\n\t}' /etc/freeradius/sites-enabled/default

###
# In case of installation of plugin RADIUS master/slave, do not enable any InMan daemon Agent
###

flag=0
IFS='"' read -ra D_INSTALL_OPTIONS <<< "$1"

for i in "${D_INSTALL_OPTIONS[@]}"; do
	OPTIONS=$(echo "$i" | sed -E -e 's/[[:blank:]]+/_/g')
	###
	### Faire la verification de savoir si on install le plugin master/slave en envoyant 
	### la liste de ce qui va etre installer. Les installeur etant libre de lire ou non la liste
	### et appliquer alors une regle ou pas
	###
	if [ "$OPTIONS" == "InMan_Radius_Cluster_plugin" ]; then
		flag=1
	fi
done

if [ "$flag" == 0 ]; then
	systemctl daemon-reload
	systemctl enable im_agent_freeradius
	systemctl start im_agent_freeradius
	systemctl enable im_agent_websocket_freeradius
	systemctl start im_agent_websocket_freeradius
else
	systemctl daemon-reload
	systemctl disable im_agent_freeradius
	systemctl stop im_agent_freeradius
	systemctl disable im_agent_websocket_freeradius
	systemctl stop im_agent_websocket_freeradius
fi

whiptail --title "For LDAP : Don't forget" --msgbox ". In /etc/freeradius/mods-available/ldap edit your configuration to correctly join your LDAP\n. Create a symbolic link between mods-available/ldap mods-enable/ldap\n. Use or uncomment ldap line in /etc/freeradius/sites-enabled/default" 15 78

systemctl reload radiusd


