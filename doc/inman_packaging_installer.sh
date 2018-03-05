#!/bin/bash

ROOTPATH=/tmp
MAINFOLDER=inman_installer
MAINPATH=$ROOTPATH/$MAINFOLDER
RADIUSPATH=$MAINPATH/install_radius_server
IMRADIUSAGENTPATH=$MAINPATH/install_inman_radius_agent/im_freeradius
IMRADIUSCLUSTERPATH=$MAINPATH/install_inman_radius_agent/im_cluster_freeradius

##
## Create tree
##
mkdir -p $MAINPATH
mkdir -p $RADIUSPATH
#mkdir -p /tmp/inman_installer/install_inman_radius_agent
mkdir -p $IMRADIUSAGENTPATH
mkdir -p $IMRADIUSCLUSTERPATH

###
# Whiptail to remember to download and place freeradius.tgz in $RADIUSPATH before proceed
###
whiptail --title "Download Freeradius sources" --scrolltext --msgbox "Download ftp://ftp.freeradius.org/pub/freeradius/freeradius-server-3.0.15.tar.gz and place freeradius-server-3.0.15.tgz in $RADIUSPATH before continue" --ok-button "Continue" 10 60

##
## Get install script from source and put into package tree
##
cp ./install_tui.sh\
  ./install_InMan_Radius_Agent.sh\
  ./install_InMan_Radius_Cluster_plugin.sh\
  ./install_Radius_server.sh\
  $MAINPATH

##
## Get element to install Freeradius
##
cp ../im_agent/im_freeradius/radiusd.service\
  ../im_agent/im_freeradius/logrotate_freeradius*\
  $RADIUSPATH

##
## Get element to install IM Agent Freeradius
##
cp -r ./python_tui_conf_agent_freeradius.py\
  ./templates\
  ../im_agent/im_freeradius/im_agent*\
  ../im_agent/im_freeradius/agent_stop_daemon_freeradius.sh\
  ../im_agent/im_freeradius/im_clientfileconfigclass_freeradius.py\
  ../im_agent/im_freeradius/radius_mod_python_conf\
  ../im_agent/im_freeradius/logrotate_im_*\
  ../im_agent/im_freeradius/logrotate_freeradius*\
  ../im_agent/im_freeradius/rlm_im_freeradius.py\
  $IMRADIUSAGENTPATH

##
## Get element to install IM Agent Cluster Freeradius
##
cp -r ./python_tui_conf_cluster_freeradius.py\
  ./templates\
  ../im_agent/im_freeradius/im_cluster*\
  ../im_agent/im_freeradius/im_agentconfigclass_freeradius.py\
  $IMRADIUSCLUSTERPATH

cd $ROOTPATH
tar cvzf InmanInstall.tgz $MAINFOLDER
