#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from configobj import ConfigObj
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
		self.websocket_urirpc = websocket_config['urirpc']
		self.websocket_radius_log = websocket_config['radius_log']
		self.websocket_log_file = websocket_config['log_file']
		self.websocket_debug_level = websocket_config['debug_level']
		


