#!/bin/bash

pid_path_agent_alive="/var/run/im/im_agent_alive_freeradius.pid"

pid_path_live_WEBSOCKET="/var/run/im/im_agent_websocket_live_freeradius.pid"
pid_path_rpc_WEBSOCKET="/var/run/im/im_agent_websocket_rpc_freeradius.pid"
pid_path_streamfile_WEBSOCKET="/var/run/im/im_agent_streamfile_freeradius.pid"

MAINPID=$2

/bin/kill -s TERM $MAINPID

if [[ $1 = "Agent" ]]; then
	/bin/kill -s TERM `cat $pid_path_agent_alive`
elif [[ $1 = "Websocket" ]]; then
	/bin/kill -s TERM `cat $pid_path_live_WEBSOCKET`
	/bin/kill -s TERM `cat $pid_path_rpc_WEBSOCKET`
	/bin/kill -s TERM `cat $pid_path_streamfile_WEBSOCKET`
fi