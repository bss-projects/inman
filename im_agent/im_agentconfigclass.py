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
		inman_config = config['Inman']

		self.agent_hostname = agent_config['name']
		self.agent_alias = agent_config['alias']
		self.agent_ip = agent_config['IP']
		self.agent_connection_type = agent_config['connection_type']
		self.agent_rpc_port = agent_config['rpc_port']

		self.dispatch_conf = local_config['dispatch_conf']
		self.service = local_config['service']
		self.bin_path = local_config['bin_path']
		self.conf_path = local_config['conf_path']
		self.services_path = local_config['services_path']
		self.hosts_path = local_config['hosts_path']

		self.inman_server = inman_config['server']


