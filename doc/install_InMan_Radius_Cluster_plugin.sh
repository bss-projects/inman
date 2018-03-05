#!/bin/bash

INMAN_DEST_MAIN_PATH="/opt/inman"
INMAN_DEST_AGENT_PATH="$INMAN_DEST_MAIN_PATH/agent_freeradius"

login="im_cluster_sync"

yum -y install sshpass

MASTER_CLUSTER_NODE=$(whiptail --inputbox "Define Master Cluster Node URL" 8 78 --title "Master Node Info" 3>&1 1>&2 2>&3)

exitstatus=$?
if [ $exitstatus = 0 ]; then
	ssh-keygen -t rsa -b 4096 -f $HOME/.ssh/im_cluster_sync_key -N ''

	###
	# whiptail alert. If you try to install this plugin far from your installation of Freeradius Agent
	###
	whiptail --scrolltext --title "!! Remember !!" --yesno "If you try to install cluster plugin 1 day after the agent you have to copy manually $HOME/.ssh/im_cluster_sync_key into authorized_keys for user $login on the master side"  --yes-button "Do it manually before press" --no-button "No need continue" 10 78
	copykey_flag=$?

	if [ $copykey_flag = 1 ]; then
		sshpass -v -p "tgbyhnuj" scp -o StrictHostKeyChecking=no $HOME/.ssh/im_cluster_sync_key.pub $login@$MASTER_CLUSTER_NODE:/home/$login/.ssh
		sshpass -v -p "tgbyhnuj" ssh -o StrictHostKeyChecking=no -t $login@$MASTER_CLUSTER_NODE "cat /home/$login/.ssh/im_cluster_sync_key.pub >> /home/$login/.ssh/authorized_keys"
		#ssh -i $HOME/.ssh/im_cluster_sync_key/im_cluster_sync_key $login@$MASTER_CLUSTER_NODE
	fi

	###
	# Compile and install Cluster plugin
	###
	cd install_inman_radius_agent/im_cluster_freeradius

	nuitka --recurse-to=im_agentconfigclass_freeradius im_clusterside_freeradius.py
	cp im_clusterside_freeradius.exe im_cluster_agent_freeradius_confcheck.cfg $INMAN_DEST_AGENT_PATH

	###
	## Calling Python TUI to create configuration file for IM Cluster Plugin
	## python tui take $MASTER_CLUSTER_NODE as input parameter
	###
	python python_tui_conf_cluster_freeradius.py "$INMAN_DEST_AGENT_PATH" "$MASTER_CLUSTER_NODE"

	cp im_cluster_plugin_freeradius.service /usr/lib/systemd/system/

	systemctl daemon-reload
	systemctl enable im_cluster_plugin_freeradius
	systemctl start im_cluster_plugin_freeradius

else
	echo "User selected Cancel."
fi

