#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import redis
import sys
import traceback
import xmlrpclib

from configobj import ConfigObj
from subprocess import Popen, call, check_call
from validate import Validator

class ConfObjClass():

	def __init__(self, configfile, configspec):
		self.configfile = configfile
		config = ConfigObj(configfile, configspec=configspec)

		validator = Validator()
		result = config.validate(validator)

		if result != True:
			print 'Config file validation failed!'
			sys.exit(1)

		agent_config = config['Agent']
		local_config = config['Local conf']
		log_config = config['Log']
		inman_config = config['Inman']
		websocket_config = config['Websocket']

		self.agent_hostname = agent_config['hostname']
		self.agent_name = agent_config['name']
		self.agent_ip = agent_config['IP']
		self.agent_connection_type = agent_config['connection_type']
		self.agent_rpc_port = agent_config['rpc_port']

		self.client_filepath = local_config['client_filepath']

		self.log_file = log_config['filename']
		self.log_debug_level = log_config['debug_level']

		self.inman_server = inman_config['server']

		self.websocket_user = websocket_config['user']
		self.websocket_pass = websocket_config['pass']
		self.websocket_router = websocket_config['router']
		self.websocket_port = websocket_config['port']
		self.websocket_realm = websocket_config['realm']
		self.websocket_uripubsub = websocket_config['uripubsub']
		self.websocket_urirpc_readfile_log = websocket_config['urirpc_readfile_log']
		self.websocket_urirpc_listfile_log = websocket_config['urirpc_listfile_log']
		self.websocket_radius_log = websocket_config['radius_log']
		self.websocket_log_file = websocket_config['log_file']
		self.websocket_debug_level = websocket_config['debug_level']
		

class ConfClusterObjClass():

	def __init__(self, configfile, configspec):
		self.configfile = configfile
		config = ConfigObj(configfile, configspec=configspec)

		validator = Validator()
		result = config.validate(validator)

		if result != True:
			print 'Config file validation failed!'
			sys.exit(1)

		plugin_config = config['Plugin']
		log_config = config['Log']
		inman_config = config['Inman']
		cluster_config = config['Cluster']

		self.plugin_hostname = plugin_config['hostname']
		self.plugin_ip = plugin_config['IP']
		self.plugin_rpc_port = plugin_config['rpc_port']

		self.log_file = log_config['filename']
		self.log_debug_level = log_config['debug_level']

		self.inman_server = inman_config['server']

		self.cluster_master_hostname = cluster_config['master_hostname']
		self.cluster_master_ip = cluster_config['master_ip']
		self.cluster_master_radius_name = cluster_config['master_radius_name']
		self.cluster_master_rpc_port = cluster_config['rpc_port']


class ManageCluster(object):
	"""docstring for ManageCluster"""
	def __init__(self, RedisPool, logging):
		super(ManageCluster, self).__init__()
		self.RedisPool = RedisPool
		self.RedisDB = redis.Redis(connection_pool=self.RedisPool)
		self.list_cluster_node = self.RedisDB.keys('cluster_node:*'.format())
		self.logging = logging
		self.rpcApi = None

	def rpcConnect(self, d_cluster_info):
		flag = True
		try:
			self.logging.info('Establish RPC connection on {0} to initiate cluster sync'.format(d_cluster_info['hostname']))
			self.rpcApi = xmlrpclib.ServerProxy('http://{0}:{1}'.format(d_cluster_info['hostname'], d_cluster_info['rpc_port']), allow_none=True)
		except Exception, e:
			self.logging.error('-- ManageCluster --\n In rpcConnect Issue : {0}\n Error stack : {1}\n'.format(e, traceback.format_exc()))
			flag = False
			pass
		return flag
		
	def launch_nodes_sync(self):
		try:
			if len(self.list_cluster_node) >= 1:
				Popen(['redis-cli save && cp /etc/freeradius/clients_im* /var/lib/redis/dump.rdb /home/im_cluster_sync'], shell=True)

			for cluster_node in self.list_cluster_node:
				self.logging.info('Get cluster node info for {0}'.format(cluster_node))
				d_cluster_info = self.RedisDB.get(cluster_node)
				d_cluster_info = ast.literal_eval(d_cluster_info)
				flag_connection = self.rpcConnect(d_cluster_info)
				if (flag_connection):
					self.rpcApi.launch_node_sync()
		except Exception, e:
			self.logging.error('-- ManageCluster --\n In launch_nodes_sync Issue : {0}\n Error stack : {1}'.format(e, traceback.format_exc()))
			pass
			

	def get_node_info(self, node_name):
		return self.RedisDB.keys('cluster_node:{0}'.format(node_name))

	def get_node_list(self):
		return self.list_cluster_node