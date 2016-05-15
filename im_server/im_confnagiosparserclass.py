#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re
import xmlrpclib

from multiprocessing import Process, Queue
from pynag.Parsers import config
from pynag import Model

class ConfNagiosParser(object):
	"""docstring for ConfNagiosParser"""

	def __init__(self, conf_file_path, d_agent_info):
		super(ConfNagiosParser, self).__init__()

		logging.debug('Init parser config for {}'.format(conf_file_path))
		Model.cfg_file = '{}'.format(conf_file_path)
		nc = config(Model.cfg_file)
		nc.parse()

		self.tunnel = None
		self.agent_connection_type = d_agent_info['agent_connection_type']
		self.d_agent_info = d_agent_info

		self.d_sc_func = {
		'RPC':
			{
				'connect': self.rpcConnect,
				'list_check': self.rpcListCheck
			},
		'SSH':
			{
				'connect': self.sshConnect,
				'list_check': self.sshListCheck
			}
		}

		self.agent_name = d_agent_info['agent_name']
		self.Model = Model
		self.Config = nc
		self.d_globalconf = {}

	def connect(self):
		logging.debug('Connect to {}'.format(self.agent_name))
		self.d_sc_func[self.agent_connection_type]['connect']()
		return

	def close(self):
		logging.debug('Close connection to {}'.format(self.agent_name))
		try:
			if self.tunnel != None:
				self.tunnel.terminate()
				self.p.terminate()
			logging.debug('Connection close for {}'.format(self.agent_name))
		except Exception, e:
			logging.error('Error during connection close for {}'.format(self.agent_name))
			raise e

	def list_check(self):
		d_checks = {}

		try:
			logging.debug('Get Check list for {}'.format(self.agent_name))
			self.connect()
			d_checks = self.d_sc_func[self.agent_connection_type]['list_check']()
			self.close()
		except Exception, e:
			logging.error('Failed to get Checks from {} : {}'.format(self.agent_name, e))
			raise e

		self.d_globalconf['checks'] = d_checks.copy()

		return d_checks

	def rpcConnect(self, port=None):
		logging.debug('Connection with RPC to {}'.format(self.agent_name))
		if port == None:
			port = self.d_agent_info['agent_rpc_port']

		try:
			self.rpcApi = xmlrpclib.ServerProxy('http://'+self.d_agent_info['agent_ip']+':'+str(port), allow_none=True)
		except Exception, e:
			logging.error('Failed to connect to {} with RPC'.format(self.agent_name))
			raise e
		return

	def initTunnel(self, q):
		logging.debug('Init SSH Tuneling for {}'.format(self.agent_name))
		tunnel = Popen(['ssh', '-L', str(self.d_agent_info['port_ssh_tunnel'])+':'+self.d_agent_info['agent_ip']+':'+str(self.d_agent_info['agent_rpc_port']), 'root@'+self.d_agent_info['agent_ip']])
		q.put(tunnel)

	def sshConnect(self, port=None):
		logging.debug('Connection through RPC for {}'.format(self.agent_name))
		if port == None:
			port = self.d_agent_info['port_ssh_tunnel']

		self.q = Queue()
		self.p = Process(target=self.initTunnel, args=(self.q,))
		self.p.start()
		try:
			self.tunnel = self.q.get()
			self.rpcApi = xmlrpclib.ServerProxy('http://127.0.0.1:'+str(port), allow_none=True)
		except Exception, e:
			logging.error('Failed to connect to {} with RPC'.format(self.agent_name))
			raise e
		return

	def rpcListCheck(self):
		logging.debug('Get Check list by RPC {}'.format(self.agent_name))
		d_checks = {}

		d_checks = self.rpcApi.list_check()

		return d_checks

	def sshListCheck(self):
		logging.debug('Get Check list through SSH for {}'.format(self.agent_name))
		d_checks = {}

		d_checks = self.rpcListCheck()

		return d_checks

	def get_all(self):

		logging.debug('Get complete config for {}'.format(self.Model.cfg_file))
		self.list_hosts()
		self.list_services()
		self.list_servicestemplate()
		self.list_hostsconfig()
		self.list_hoststemplate()
		self.list_resources()
		self.list_command()
		self.list_check()

		return self.d_globalconf

	def list_resources(self):

		logging.debug('Get Resources list for {}'.format(self.Model.cfg_file))
		self.Model.ObjectFetcher.reload_cache

		d_resources = {}

		all_resources = self.Config.get_resources()
		for i in all_resources:
			if i[0] != None:
				d_resources[i[0]] = i[1]

		self.d_globalconf['resources'] = d_resources.copy()
		return d_resources

	def list_hosts(self):

		logging.debug('Get Hosts list for {}'.format(self.Model.cfg_file))
		self.Model.ObjectFetcher.reload_cache

		d_hosts = {}

		all_hosts = self.Model.Host.objects.all
		for i in all_hosts:
			if i.host_name != None:
				d_hosts[i.host_name] = i.host_name

		self.d_globalconf['hosts'] = d_hosts.copy()
		return d_hosts

	def list_services(self):

		logging.debug('Get Services list for {}'.format(self.Model.cfg_file))
		self.Model.ObjectFetcher.reload_cache

		d_services = {}

		service_list = self.Model.Service.objects.all

		for service in service_list:
			if service.host_name != None:
				d_services[service.service_description] = service._defined_attributes.copy()
				del d_services[service.service_description]['host_name']

		self.d_globalconf['services'] = d_services.copy()
		return d_services

	def list_servicestemplate(self):

		logging.debug('Get Templates Services list for {}'.format(self.Model.cfg_file))
		self.Model.ObjectFetcher.reload_cache

		d_servicestemplate = {}

		service_list = self.Model.Service.objects.all

		for service in service_list:
			if service.host_name == None:
				d_servicestemplate[service.name] = service._defined_attributes.copy()

		self.d_globalconf['servicestemplate'] = d_servicestemplate.copy()
		return d_servicestemplate

	def list_command(self):

		logging.debug('Get Command list for {}'.format(self.Model.cfg_file))
		self.Model.ObjectFetcher.reload_cache

		d_command = {}

		command_list = self.Model.Command.objects.all

		logging.debug('List of command for {} : {}'.format(self.Model.cfg_file, self.Model.Command.objects.get_all()))

		for command in command_list:
			d_command[command.command_name] = command._defined_attributes.copy()

		self.d_globalconf['command'] = d_command.copy()
		return d_command

	def list_hostsconfig(self):

		logging.debug('Get Hosts config for {}'.format(self.Model.cfg_file))
		self.Model.ObjectFetcher.reload_cache

		d_hostsconfig = {}
		l_entryToTab = ('use', 'parents')
		hostgroups = []

		###
		# @ToDo Faire un test le meme nom de host sur deux superviseurs différents
		# voir s'il y a conflit ou double enregistrement
		###

		all_hosts = self.Model.Host.objects.all
		for i in all_hosts:
			if i.host_name != None:
				logging.debug('Get {} config'.format(i.host_name))
				d_hostsconfig[i.host_name] = i._defined_attributes.copy()

				for entry in l_entryToTab:
					if entry in d_hostsconfig[i.host_name]:
						d_hostsconfig[i.host_name][entry] = d_hostsconfig[i.host_name][entry].split(',')

				logging.debug('Get {} entry config: {}'.format(i.host_name, d_hostsconfig[i.host_name]))

				l_hostgroups = i.get_effective_hostgroups()
				logging.debug('Get {} hostgroups to convert: {}'.format(i.host_name, l_hostgroups))
				hostgroups = []
				for hostgroup in l_hostgroups:
					logging.debug('Get {} hostgroup: {}'.format(i.host_name, hostgroup.hostgroup_name))
					hostgroups.append(hostgroup.hostgroup_name)
				d_hostsconfig[i.host_name]['hostgroups'] = hostgroups

				d_hostsconfig[i.host_name]['filepath'] = i.get_filename()

				if i.parents == None:
					d_hostsconfig[i.host_name]['parents'] = i.parents

	#			d_hostsconfig[i.host_name] = {'host_name': i.host_name}
	#			d_hostsconfig[i.host_name]['use'] = i.use.split(',')
	#			d_hostsconfig[i.host_name]['address'] = i.address
	#			d_hostsconfig[i.host_name]['alias'] = i.alias
	#			d_hostsconfig[i.host_name]['filepath'] = i.get_filename()
	#			if i.parents != None:
	#				d_hostsconfig[i.host_name]['parents'] = i.parents.split(',')
	#			else:
	#				d_hostsconfig[i.host_name]['parents'] = i.parents

				###
				# Attention ici le substr est fait pour virer le + si pas de plus il ne faut pas faire de substr
				###
	#			d_hostsconfig[i.host_name]['hostgroups'] = i.hostgroups[1:].split(',')

				l_macro = []
				for key, value in i._defined_attributes.items():
					if re.search("^_", key, re.IGNORECASE) is not None:
						l_macro.append({'name': key, 'value': value})
				d_hostsconfig[i.host_name]['macros'] = l_macro

				service_list = self.Model.Service.objects.filter(host_name=i.host_name)
				l_service = [] 
				for service in service_list:
					infoService = service._defined_attributes.copy()
					infoService['filepath'] = service.get_filename()
					l_service.append(infoService)

				d_hostsconfig[i.host_name]['services'] = l_service
				d_hostsconfig[i.host_name]['supervisor_name'] = self.agent_name

		self.d_globalconf['hostsconfig'] = d_hostsconfig.copy()
		return d_hostsconfig

	def list_hoststemplate(self):

		logging.debug('Get Template Hosts for {}'.format(self.Model.cfg_file))
		self.Model.ObjectFetcher.reload_cache

		d_hoststemplate = {}

		all_hosts = self.Model.Host.objects.all
		for i in all_hosts:
			if i.host_name == None:
				d_hoststemplate[i.name] = i._defined_attributes.copy()

		self.d_globalconf['hoststemplate'] = d_hoststemplate.copy()
		return d_hoststemplate

class ConfNagiosDB(object):
	"""docstring for ConfNagiosDB"""
	def __init__(self, IMDB, ConfNagiosData):
		super(ConfNagiosDB, self).__init__()
		self.IMDB = IMDB
		self.ConfNagiosData = ConfNagiosData
		