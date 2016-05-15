#!/usr/bin/python
# -*- coding: utf-8 -*-

import im_agentconfigclass_supervisor
import json
import logging
import os
import re
import setproctitle
import shutil
import time
import urllib2

from multiprocessing import Process, Queue
from pprint import pprint
from pynag.Control import daemon
from pynag.Parsers import config
from pynag import Model, Utils
from SimpleXMLRPCServer import SimpleXMLRPCServer
from subprocess import Popen, PIPE

def get_synopsis(command):
	try:
		logging.debug('Get synopsis for "{0}"'.format(command))
		p = Popen([command, '--help'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate()
		rc = p.returncode
		return output, err
	except Exception, e:
		logging.error('Failed to get synopsis "{0}" : {1}'.format(command, e))
		return '', 'Failed for "{0}": {1}'.format(command, e)

def list_check():

	try:

		global Conf

		error = synopsis = ''
		d_ret = {}

		logging.info('Get check from {0}'.format(Conf.libexec_path))

		for dirname, dirnames, filenames in os.walk(Conf.libexec_path):
			for filename in filenames:
				path = ''
				path = os.path.join(dirname, filename)
				flag = 'Not'
				if os.access(path, os.X_OK):
					flag = 'Exec'
					synopsis, error = get_synopsis(path)
					d_ret[filename] = synopsis
	
		return d_ret
	except Exception, e:
		logging.error('Failed to get list of check : {0}'.format(e))
		return d_ret


def master_alive():
	try:
		global Conf

		pid = os.getpid()

		if not os.path.isfile('/var/run/im/im_agent_alive_supervisor.pid'):
			path, filename = os.path.split('/var/run/im/im_agent_alive_supervisor.pid')
			os.makedirs(path)
			open('/var/run/im/im_agent_alive_supervisor.pid', 'a').close()

		fd = open('/var/run/im/im_agent_alive_supervisor.pid', 'w')
		fd.write(str(pid))
		fd.close()

		flag = 0 #le contact a eu lieu remise a 0 qd contact perdu

		headers = {'Content-Type': 'application/json'}

		query_args = {'agent_hostname': Conf.agent_hostname, 'agent_name': Conf.agent_name, 'agent_ip': Conf.agent_ip, 'agent_connection_type': Conf.agent_connection_type, 'agent_rpc_port': Conf.agent_rpc_port, 'agent_conf_path': Conf.agent_conf_path, 'agent_conf_file': Conf.agent_conf_file, 'plugin': 'supervisor'}

		data = json.dumps(query_args)

		url_register = 'http://'+Conf.inman_server+'/register_agent_new'
		url_alive = 'http://'+Conf.inman_server+'/im_masteralive'

		# Send HTTP POST request
		request_alive = urllib2.Request(url_alive, data, headers)
		request_register = urllib2.Request(url_register, data, headers)

		while 1:
			try:
				if flag == 0:
					response = urllib2.urlopen(request_register)
					logging.info('Register agent : {0} to {1}'.format(Conf.agent_name, Conf.inman_server))
					flag = 1
				else:
					response = urllib2.urlopen(request_alive)
					time.sleep(1)
			except urllib2.URLError, e:
				logging.error('Connection error to {0} for {1} : {2}'.format(Conf.inman_server, Conf.agent_name, e))
				flag = 0
				time.sleep(1)
	except KeyboardInterrupt:
		logging.info('Exiting Alive process : {0} to {1}'.format(Conf.agent_name, Conf.inman_server))

##**********************##
## MAIN                 ##
##**********************##

setproctitle.setproctitle('IM Agent Supervisor')

try:
	
	Conf = im_agentconfigclass_supervisor.ConfObjClass('im_agent_supervisor.cfg', 'im_agent_supervisor_confcheck.cfg')
	
	if not os.path.isfile(Conf.log_file):
		path, filename = os.path.split(Conf.log_file)
		os.makedirs(path)
		open(Conf.log_file, 'a').close()
	
	logging.basicConfig(level=eval(Conf.log_debug_level), filename=Conf.log_file, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

	server = SimpleXMLRPCServer(('0.0.0.0', Conf.agent_rpc_port), logRequests=True, allow_none=True)

	server.register_function(master_alive)
	server.register_function(list_check)

except Exception, e:
	logging.error('Failed to init agent {0} -> {1}'.format(Conf.agent_name, e))
	raise e


try:
	print 'Use Control-C to exit'
	logging.info('Start Agent : {0}'.format(Conf.agent_name))
	#### *****************************
	## Send information to Inman master to declare the agent
	#### *****************************
	p = Process(target=master_alive)
	p.start()
	server.serve_forever()
except KeyboardInterrupt:
	logging.info('Exiting Agent : {0}'.format(Conf.agent_name))
