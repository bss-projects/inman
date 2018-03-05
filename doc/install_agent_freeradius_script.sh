#!/bin/bash

SERVER_DEST="srv_agent_radius.inman.lan"
INMAN_SOURCE_PATH="/root/inman/git"
INMAN_SOURCE_AGENT_PATH="$INMAN_SOURCE_PATH/im_agent/im_freeradius"
INMAN_DEST_SOURCE_PATH="/tmp/inman_source"

INMAN_DEST_MAIN_PATH="/opt/inman"
INMAN_DEST_AGENT_PATH="$INMAN_DEST_MAIN_PATH/agent_freeradius"

OLD_VERSION="v0.9.4-RC2"

ssh root@$SERVER_DEST "mkdir -p $INMAN_DEST_SOURCE_PATH"
scp -r $INMAN_SOURCE_AGENT_PATH root@$SERVER_DEST:$INMAN_DEST_SOURCE_PATH

ssh root@$SERVER_DEST "cd $INMAN_DEST_SOURCE_PATH/im_freeradius && nuitka --recurse-to=im_clientfileconfigclass_freeradius --recurse-to=im_agentconfigclass_freeradius im_agentside_freeradius.py"
ssh root@$SERVER_DEST "cd $INMAN_DEST_SOURCE_PATH/im_freeradius && nuitka --recurse-to=im_agentconfigclass_freeradius im_agentside_websocket_freeradius.py"

ssh root@$SERVER_DEST "mkdir -p $INMAN_DEST_AGENT_PATH"
ssh root@$SERVER_DEST "cp -r $INMAN_DEST_AGENT_PATH $INMAN_DEST_AGENT_PATH/../inman_agent_freeradius.$OLD_VERSION"
ssh root@$SERVER_DEST "cd $INMAN_DEST_SOURCE_PATH/im_freeradius && cp im_agentside_freeradius.exe im_agentside_websocket_freeradius.exe init.d_im_agent_freeradius logrotate_freeradius logrotate_freeradius_log logrotate_im_freeradius rlm_im_freeradius.py $INMAN_DEST_AGENT_PATH"
ssh root@$SERVER_DEST "cp $INMAN_DEST_AGENT_PATH/rlm_im_freeradius.py /usr/local/lib/python2.7/dist-packages"
