#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import setproctitle
import redis
import traceback
import xmlrpclib

from im_agentconfigclass_freeradius import ConfClusterObjClass
from multiprocessing import Process, Queue
from SimpleXMLRPCServer import SimpleXMLRPCServer
from subprocess import Popen, PIPE, call, check_call

def launch_node_sync():
	global Conf
	stdout = ''
	stderrno = ''

	try:
		logging.info('Launch node sync from {0} for {1}'.format(Conf.cluster_master_hostname, Conf.cluster_master_radius_name))
		
		sp_radius = Popen(['systemctl stop redis'], shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderrno = sp_radius.communicate()
		if stdout != '' or stderrno != '':
			logging.info('Stop Redis STDOUT: {0}\nSTDERRNO: {1}'.format(stdout, stderrno))

		sp_redis = Popen(['scp -i /root/.ssh/im_cluster_sync_key im_cluster_sync@{0}:dump.rdb /var/lib/redis/'.format(Conf.cluster_master_hostname)], shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderrno = sp_redis.communicate()
		if stdout != '' or stderrno != '':
			logging.info('SCP Redis STDOUT: {0}\nSTDERRNO: {1}'.format(stdout, stderrno))

		sp_radius = Popen(['scp -i /root/.ssh/im_cluster_sync_key im_cluster_sync@{0}:clients_im* /etc/freeradius/'.format(Conf.cluster_master_hostname)], shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderrno = sp_radius.communicate()
		if stdout != '' or stderrno != '':
			logging.info('SCP Radius STDOUT: {0}\nSTDERRNO: {1}'.format(stdout, stderrno))


		sp_redis = Popen(['systemctl restart radiusd'], shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderrno = sp_redis.communicate()
		if stdout != '' or stderrno != '':
			logging.info('Restart Radius STDOUT: {0}\nSTDERRNO: {1}'.format(stdout, stderrno))


		sp_radius = Popen(['systemctl start redis'], shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderrno = sp_radius.communicate()
		if stdout != '' or stderrno != '':
			logging.info('Start Redis STDOUT: {0}\nSTDERRNO: {1}'.format(stdout, stderrno))

		### scp -i /root/.ssh/im_cluster_sync_key im_cluster_sync@Conf.cluster_master_hostname:dump.rdb /var/lib/redis/
		### scp -i /root/.ssh/im_cluster_sync_key im_cluster_sync@Conf.cluster_master_hostname:client_im* /etc/freeradius/
		### systemctl restart radius
		### systemctl restart redis
	except Exception, e:
		sp_radius = Popen(['systemctl start redis'], shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderrno = sp_radius.communicate()
		if stdout != '' or stderrno != '':
			logging.info('Start Redis STDOUT: {0}\nSTDERRNO: {1}'.format(stdout, stderrno))
		logging.error('-- ClusterSyncSide --\n In launch_nodes_sync Issue : {0}\n Error stack : {1}\nSTDOUT: {2}\nSTDERR: {3}'.format(e, traceback.format_exc(), stdout, stderrno))
		pass

##**********************##
## MAIN                 ##
##**********************##

setproctitle.setproctitle('IM Cluster Agent Freeradius')

### cluster_node : network_identifier = ip or FQDN
### os.system('sudo apt-get update')

try:
	Conf = ConfClusterObjClass('im_cluster_agent_freeradius.cfg', 'im_cluster_agent_freeradius_confcheck.cfg')
	
	if not os.path.isfile(Conf.log_file):
		path, filename = os.path.split(Conf.log_file)
		if not os.path.isdir(path):
			os.makedirs(path)
		open(Conf.log_file, 'a').close()
	
	logging.basicConfig(level=eval(Conf.log_debug_level), filename=Conf.log_file, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

	logging.info('Start Cluster plugin : Try registration on {0}, RADIUS -> {1}'.format(Conf.cluster_master_hostname, Conf.cluster_master_radius_name))

	rpcApi = xmlrpclib.ServerProxy('http://'+Conf.cluster_master_hostname+':'+str(Conf.cluster_master_rpc_port), allow_none=True)
	status, errno = rpcApi.register_cluster_node({'hostname': Conf.plugin_hostname, 'info': {'hostname': Conf.plugin_hostname, 'ip': Conf.plugin_ip, 'rpc_port': Conf.plugin_rpc_port}})

	if status == True:
		logging.info('Success: {0}'.format(errno))
	else:
		logging.error('-- Main RPC Loop --\n Issue : {0}'.format(errno))
		sys.exit()
					

	server = SimpleXMLRPCServer(('0.0.0.0', Conf.plugin_rpc_port), logRequests=True, allow_none=True)
	server.register_function(launch_node_sync)
	server.serve_forever()
except Exception, e:
	logging.error('-- Main RPC Loop --\n Issue : {0}\n Error stack : {1}\n'.format(e, traceback.format_exc()))
	raise e