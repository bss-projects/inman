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

		master_config = config['Master']
		local_config = config['Local conf']
		log_config = config['Log']
		svn_config = config['SVN']
		websoc_config = config['Websocket']

		self.master_hostname = master_config['hostname']
		self.master_url = master_config['url']
		self.master_ip = master_config['IP']
		self.master_web_port = master_config['web_port']
		self.master_rpc_wpub_port = master_config['rpc_wpub_port']

		self.translation = local_config['translation']
		self.CAS_SERVER = local_config['CAS_SERVER']
		self.SERVICE_URL = local_config['SERVICE_URL']

		self.log_file = log_config['filename']
		self.scp_log_file = log_config['filename_scp']
		self.rpc_log_file = log_config['filename_rpc']
		self.parser_log_file = log_config['filename_parser']
		self.log_debug_level = log_config['debug_level']

		self.svn_server = svn_config['svn_server']
		self.svn_repo = svn_config['svn_repo']

		self.websocket_user = websoc_config['user']
		self.websocket_pass = websoc_config['pass']
		self.websocket_router = websoc_config['router']
		self.websocket_port = websoc_config['port']
		self.websocket_realm = websoc_config['realm']
		self.websocket_uriparser = websoc_config['uriparser']
		self.websocket_uriscp = websoc_config['uriscp']