#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import signal
import time
import xmlrpclib
from multiprocessing import Process, Queue
from pprint import pprint
from subprocess import Popen, call, check_call

class ClassAgent(object):
	"""docstring for ClassAgent"""

####
# Faire un init qui prend en param le nom d'un agent (agent_alias) comme ca 
# l'objet sera init avec les infos en DB
####

	def __init__(self, d_agent_info, db_instance, agent_alias=None):
		super(ClassAgent, self).__init__()
		self.tunnel = None
		self.d_agent_info = d_agent_info
		self.agent_connection_type = d_agent_info['agent_connection_type']
		self.db_instance = db_instance
		self.d_sc_func = {
		'RPC':
			{
				'connect': self.rpcConnect,
				'getListHosts': self.rpcListHosts,
				'getListHostsconfig': self.rpcListHostsconfig,
				'getListHoststemplate': self.rpcListHoststemplate,
				'getListServices': self.rpcListServices,
				'getListServicestemplate': self.rpcListServicestemplate,
				'getProgressSync': self.rpcGetProgressSync,
				'initSyncSupervisor': self.rpcInitSyncSupervisor
			},
		'SSH':
			{
				'connect': self.sshConnect,
				'getListHosts': self.sshListHosts,
				'getListHostsconfig': self.sshListHostsconfig,
				'getListHoststemplate': self.sshListHoststemplate,
				'getListServices': self.sshListServices,
				'getListServicestemplate': self.sshListServicestemplate,
				'getProgressSync': self.sshGetProgressSync,
				'initSyncSupervisor': self.sshInitSyncSupervisor
			}
		}


	def connect(self):
		self.d_sc_func[self.agent_connection_type]['connect']()
		return

	def close(self):
		try:
			if self.tunnel != None:
				self.tunnel.terminate()
				self.p.terminate()
		except Exception, e:
			raise e

	def getAllconf(self):
		self.d_all_conf = {}

		self.d_all_conf['listHosts'] = self.getListHosts()
		self.d_all_conf['listHostsconfig'] = self.getListHostsconfig()
		self.d_all_conf['listHoststemplate'] = self.getListHoststemplate()
		self.d_all_conf['listServices'] = self.getListServices()
		self.d_all_conf['listServicestemplate'] = self.getListServicestemplate()
		return self.d_all_conf

	def getListHosts(self):
		self.d_sc_func[self.agent_connection_type]['getListHosts']()
		return self.listHosts

	def getListHostsconfig(self):
		self.d_sc_func[self.agent_connection_type]['getListHostsconfig']()
		return self.listHostsconfig

	def getListHoststemplate(self):
		self.d_sc_func[self.agent_connection_type]['getListHoststemplate']()
		return self.listHoststemplate

	def getListServices(self):
		self.d_sc_func[self.agent_connection_type]['getListServices']()
		return self.listServices

	def getListServicestemplate(self):
		self.d_sc_func[self.agent_connection_type]['getListServicestemplate']()
		return self.listServicestemplate

	def getProgressSync(self):
		self.d_sc_func[self.agent_connection_type]['getProgressSync']()
		return self.progressSyncInfo

	def agentalive(self):
		return

	def initSyncSupervisor(self, collection2Sync):
		self.d_sc_func[self.agent_connection_type]['initSyncSupervisor'](collection2Sync)
		return

	def rpcConnect(self, port=None):
		if port == None:
			port = self.d_agent_info['agent_rpc_port']

		try:
			self.rpcApi = xmlrpclib.ServerProxy('http://'+self.d_agent_info['agent_ip']+':'+str(port), allow_none=True)
		except Exception, e:
			raise e
		return

	def initTunnel(self, q):
		tunnel = Popen(['ssh', '-L', str(self.d_agent_info['port_ssh_tunnel'])+':'+self.d_agent_info['agent_ip']+':'+str(self.d_agent_info['agent_rpc_port']), 'root@'+self.d_agent_info['agent_ip']])
		q.put(tunnel)

	def sshConnect(self, port=None):
		if port == None:
			port = self.d_agent_info['port_ssh_tunnel']

		self.q = Queue()
		self.p = Process(target=self.initTunnel, args=(self.q,))
		self.p.start()
		try:
			self.tunnel = self.q.get()
			self.rpcApi = xmlrpclib.ServerProxy('http://127.0.0.1:'+str(port), allow_none=True)
		except Exception, e:
			raise e
		return

	def rpcInitSyncSupervisor(self, collection2Sync):
		self.rpcApi.sync_conf(collection2Sync)
		return

	def sshInitSyncSupervisor(self, collection2Sync):
		self.rpcInitSyncSupervisor(collection2Sync)
		return

	def rpcListHosts(self):
		try:
			self.listHosts = self.rpcApi.list_hosts()
		except Exception, e:
			print e.__dict__
			raise e
		return

	def sshListHosts(self):
		self.rpcListHosts()
		return

	def rpcListHostsconfig(self):
		self.listHostsconfig = self.rpcApi.list_hostsconfig()
		return

	def sshListHostsconfig(self):
		self.rpcListHostsconfig()
		return

	def rpcListHoststemplate(self):
		self.listHoststemplate = self.rpcApi.list_hoststemplate()
		return

	def sshListHoststemplate(self):
		self.rpcListHoststemplate()
		return

	def rpcListServices(self):
		self.listServices = self.rpcApi.list_services()
		return

	def sshListServices(self):
		self.rpcListServices()
		return

	def rpcListServicestemplate(self):
		self.listServicestemplate = self.rpcApi.list_servicestemplate()
		return

	def sshListServicestemplate(self):
		self.rpcListServicestemplate()
		return

	def rpcGetProgressSync(self):
		self.progressSyncInfo = self.rpcApi.get_progress_sync()
		return

	def sshGetProgressSync(self):
		self.rpcGetProgressSync()
		return




class ClassAgentFreeradius(object):
	"""docstring for ClassAgent"""

####
# Faire un init qui prend en param le nom d'un agent (agent_name) comme ca 
# l'objet sera init avec les infos en DB
####

	def __init__(self, d_agent_info, db_instance, agent_name=None):
		super(ClassAgentFreeradius, self).__init__()
		self.tunnel = None
		self.d_agent_info = d_agent_info
		self.agent_connection_type = d_agent_info['agent_connection_type']
		self.db_instance = db_instance
		self.d_sc_func = {
		'RPC':
			{
				'connect': self.rpcConnect,
				'getProgressSync': self.rpcGetProgressSync,
				'initSync': self.rpcInitSync,
				'isAgentAlive' : self.rpcAgentAlive
			},
		'SSH':
			{
				'connect': self.sshConnect,
				'getProgressSync': self.sshGetProgressSync,
				'initSync': self.sshInitSync,
				'isAgentAlive' : self.sshAgentAlive
			}
		}


	def connect(self):
		self.d_sc_func[self.agent_connection_type]['connect']()
		return

	def close(self):
		try:
			if self.tunnel != None:
				self.tunnel.terminate()
				self.p.terminate()
		except Exception, e:
			raise e

	def getAllconf(self):
		self.d_all_conf = {}

		return self.d_all_conf

	def getProgressSync(self):
		self.d_sc_func[self.agent_connection_type]['getProgressSync']()
		return self.progressSyncInfo

	def agentalive(self):
		if self.d_sc_func[self.agent_connection_type]['isAgentAlive']():
			return True
		else:
			return False

	def initSync(self, collection2Sync):
		self.d_sc_func[self.agent_connection_type]['initSync'](collection2Sync)
		return

	def rpcConnect(self, port=None):
		if port == None:
			port = self.d_agent_info['agent_rpc_port']

		try:
			self.rpcApi = xmlrpclib.ServerProxy('http://'+self.d_agent_info['agent_ip']+':'+str(port), allow_none=True)
		except Exception, e:
			raise e
		return

	def initTunnel(self, q):
		try :
			tunnel = Popen(['ssh', '-L', str(self.d_agent_info['port_ssh_tunnel'])+':'+self.d_agent_info['agent_ip']+':'+str(self.d_agent_info['agent_rpc_port']), 'root@'+self.d_agent_info['agent_ip']])
			q.put(tunnel)
		except Exception, e:
			os.killpg(tunnel.pid, signal.SIGTERM)
			raise e

	def sshConnect(self, port=None):
		if port == None:
			port = self.d_agent_info['port_ssh_tunnel']

		self.q = Queue()
		self.p = Process(target=self.initTunnel, args=(self.q,))
		self.p.start()
		try:
			self.tunnel = self.q.get(True, 30)
			self.rpcApi = xmlrpclib.ServerProxy('http://127.0.0.1:'+str(port), allow_none=True)
		except Exception, e:
			raise e
		return

	def rpcInitSync(self, collection2Sync):
		self.rpcApi.sync_conf(collection2Sync)
		return

	def sshInitSync(self, collection2Sync):
		self.rpcInitSync(collection2Sync)
		return

	def rpcGetProgressSync(self):
		self.progressSyncInfo = self.rpcApi.get_progress_sync()
		return

	def sshGetProgressSync(self):
		self.rpcGetProgressSync()
		return

	def rpcAgentAlive(self):
		return self.rpcApi.agent_alive()

	def sshAgentAlive(self):
		return self.rpcAgentAlive()