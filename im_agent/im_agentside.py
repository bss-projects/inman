#!/usr/bin/python
# -*- coding: utf-8 -*-

import im_agentconfigclass
import json
import logging
import os
import os.path
import re
import setproctitle
import shutil
import time
import urllib2
from multiprocessing import Process, Queue
from os.path import isfile, join
from pynag.Control import daemon
from pynag.Parsers import config
from pynag import Model, Utils
from SimpleXMLRPCServer import SimpleXMLRPCServer
from subprocess import Popen

from pprint import pprint

# Expose a function

def list_hosts():
	global Conf
	global Model

	Model.ObjectFetcher.reload_cache

	d_hosts = {}

	all_hosts = Model.Host.objects.all
	for i in all_hosts:
		if i.host_name != None:
			d_hosts[i.host_name] = i.host_name

	return d_hosts

def list_services():
	global Conf
	global Model

	Model.ObjectFetcher.reload_cache

	d_services = {}

	service_list = Model.Service.objects.all

	for service in service_list:
		if service.host_name != None:
			d_services[service.service_description] = service._defined_attributes.copy()
			del d_services[service.service_description]['host_name']

	return d_services

def list_servicestemplate():
	global Conf
	global Model

	Model.ObjectFetcher.reload_cache

	d_servicestemplate = {}

	service_list = Model.Service.objects.all

	for service in service_list:
		if service.host_name == None:
			d_servicestemplate[service.name] = service._defined_attributes.copy()

	return d_servicestemplate

def list_hostsconfig():
	global Conf
	global Model

	Model.ObjectFetcher.reload_cache

	d_hostsconfig = {}
	l_entryToTab = ('use', 'parents')
	hostgroups = []

	###
	# @ToDo Faire un test le meme nom de host sur deux superviseurs différents
	# voir s'il y a conflit ou double enregistrement
	###

	all_hosts = Model.Host.objects.all
	for i in all_hosts:
		if i.host_name != None:
			d_hostsconfig[i.host_name] = i._defined_attributes.copy()

			for entry in l_entryToTab:
				if entry in d_hostsconfig[i.host_name]:
					d_hostsconfig[i.host_name][entry] = d_hostsconfig[i.host_name][entry].split(',')

			l_hostgroups = i.get_effective_hostgroups()
			hostgroups = []
			for hostgroup in l_hostgroups:
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

			service_list = Model.Service.objects.filter(host_name=i.host_name)
			l_service = [] 
			for service in service_list:
				infoService = service._defined_attributes.copy()
				infoService['filepath'] = service.get_filename()
				l_service.append(infoService)

			d_hostsconfig[i.host_name]['services'] = l_service
			d_hostsconfig[i.host_name]['supervisor_name'] = Conf.agent_alias

	return d_hostsconfig

def list_hoststemplate():
	global Conf
	global Model

	Model.ObjectFetcher.reload_cache

	d_hoststemplate = {}

	all_hosts = Model.Host.objects.all
	for i in all_hosts:
		if i.host_name == None:
			d_hoststemplate[i.name] = i._defined_attributes.copy()

	return d_hoststemplate

def agent_alive():
	try:
		global Conf
		global Model

		flag = 0 #le contact a eu lieu remise a 0 qd contact perdu

		headers = {'Content-Type': 'application/json'}

		query_args = {'agent_hostname': Conf.agent_hostname, 'agent_alias': Conf.agent_alias, 'agent_ip': Conf.agent_ip, 'agent_connection_type': Conf.agent_connection_type, 'agent_rpc_port': Conf.agent_rpc_port}

		data = json.dumps(query_args)

		url_register = 'http://'+Conf.inman_server+'/register_agent'
		url_alive = 'http://'+Conf.inman_server+'/im_masteralive'

		# Send HTTP POST request
		request_alive = urllib2.Request(url_alive, data, headers)
		request_register = urllib2.Request(url_register, data, headers)

		while 1:
			try:
				if flag == 0:
					response = urllib2.urlopen(request_register)
					flag = 1
				else:
					response = urllib2.urlopen(request_alive)
					time.sleep(1)
			except urllib2.URLError, e:
				flag = 0
				time.sleep(1)
	except KeyboardInterrupt:
		print 'Exiting Alive process'

def push_progress(status, message, percent):

	headers = {'Content-Type': 'application/json'}

	progress_args = {'status': status, 'message': message, 'progress': percent, 'agent_alias': Conf.agent_alias}

	progress_data = json.dumps(progress_args)

	url_push_progress = 'http://'+Conf.inman_server+'/pushprogresssync'

	# Send HTTP POST request
	request_push_progress = urllib2.Request(url_push_progress, progress_data, headers)

	response = urllib2.urlopen(request_push_progress)

def restart_monitoring():
	global Conf
	global Model

	try:
		res = Utils.runCommand(Conf.service + ' restart', raise_error_on_fail=True)
		push_progress('success', 'Relance du logiciel de supervision', 40)
		time.sleep(1)
		push_progress('end', 'Synchronization complete', 100)
	except Exception, e:
		push_progress('failed', 'Echec du redémarrage du logiciel de supervision', 40)
#		push_progress('end', 'end', 100)
		raise e
		
#	service = Popen([Conf.service, 'restart', '>', 'monitoring_restart.log'])

def pre_flight_check():

	#########
	## @ToDo
	## Reprendre le confPath et binPath du fichier de conf de l'agent
	#########

	try:
		res = Utils.runCommand('/usr/local/shinken/bin/shinken-arbiter -v -c /usr/local/shinken/etc/nagios.cfg -c /usr/local/shinken/etc/shinken-specific.cfg', raise_error_on_fail=True)
		push_progress('success', 'Vérification de la nouvelle configuration', 30)
		restart_monitoring()
	except Exception, e:
		push_progress('failed', 'Nouvelle configuration de supervision incorrecte', 30)
		push_progress('end', 'end', 100)
		raise e

def delete_regex(path, pattern):
	for f in os.listdir(path):
		if re.search(pattern, f):
			os.remove(os.path.join(path, f))

def save_conf_file(path, pattern):
	l_copy_file = []

	for f in os.listdir(path):
		file_path = join(path,f)
		if os.path.isfile(file_path):
			if re.search(pattern, f):
				l_copy_file.append(f+'.bck')
				shutil.copy(file_path, file_path+'.bck')

def save_in_file(collection_data):

	ommit = ['filepath', 'supervisor_name']
	to_loop = ['use', 'macros', 'hostgroups', 'parents', 'services']
	block_service = ''
	
	list_path = []
	l_copy_file = []

	try:
		for key, value in collection_data.items():
			info = value[key]
			if info['filepath'] != '':
				path, filename = os.path.split(info['filepath'])
			else:
				filepath_hosts = Conf.hosts_path
				filepath_services = Conf.services_path

			if Conf.dispatch_conf and info['filepath'] != '':
				filepath_services = filepath_hosts = join(path, key+'.cfg')

				if path not in list_path:
					list_path.append(path)
					save_conf_file(path, '(\.cfg)$')
					delete_regex(path, '(\.cfg)$')

				fd = file(filepath_hosts, 'w+')
				fd.write("define host{\n")
				for key, value in info.items():
					if key not in ommit:
						if key in to_loop:
							if key == 'services':
								for service in value:
									block_service += 'define service{'+"\n"
										for name, valo in service.items():
											if name not in ommit:
												block_service += '\t'+name+'\t'+valo+"\n"
											block_service += '}'+"\n"
							elif key == 'macros':
								for macro in value:
									fd.write('\t'+macro['name']+'\t'+macro['value']+"\n")
							elif value and len(value) :
								if key != 'use':
									val = '+'
								else:
									val = ''

								for data in value: 
									val += data

								if val != '+' and val != '':
									fd.write('\t'+key+'\t'+val+"\n")
						elif value:
							fd.write('\t'+key+'\t'+value+"\n")
				fd.write('}'+"\n")
	            
				if block_service != '':
					fd.write(block_service)
					block_service = ''
				fd.close

			elif Conf.dispatch_conf == False and info['filepath'] != '':
				filepath_hosts = info['filepath']

		push_progress('success', 'Création des fichiers de configuration', 23)

		time.sleep(2)
		pre_flight_check()

	except Exception, e:
		push_progress('failed', 'Création des nouveaux fichiers de configuration impossible', 23)
		push_progress('end', 'end', 100)
		raise e


	

def sync_conf(collection2Sync):
	global Conf
	global Model

	try:
		headers = {'Content-Type': 'application/json'}
		query_args = {'agent_alias': Conf.agent_alias, 'collection2Sync': collection2Sync}
		data = json.dumps(query_args)

		url_sync_conf = 'http://'+Conf.inman_server+'/syncconf'

		# Send HTTP POST request
		request_sync_conf = urllib2.Request(url_sync_conf, data, headers)
		response = urllib2.urlopen(request_sync_conf)
		collection_data = json.loads(json.loads(response.read()))

		push_progress('success', 'Récupération des données sur le superviseur', 22)
		time.sleep(2)
		save_in_file(collection_data)
	except Exception, e:
		push_progress('failed', 'Echec de la récupération des données', 22)
		push_progress('end', 'end', 100)
		raise e
	

#########
##	Progress['status'] = 'success' / 'failed'
##	Progress['message'] = 'Operation reussie' # message d'avancement
##	Progress['progress'] = 23 # valeur de la progression
##	Progress['return'] = False # au moment de l'ecriture du message. True quand le message est envoye
#########

setproctitle.setproctitle('IM Agent')

Conf = im_agentconfigclass.ConfObjClass('im_agent.cfg', 'im_agent_confcheck.cfg')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

## Create the plugin option
Model.cfg_file = Conf.conf_path
nc = config(Conf.conf_path)
nc.parse()

server = SimpleXMLRPCServer(('0.0.0.0', Conf.agent_rpc_port), logRequests=True, allow_none=True)

server.register_function(list_hosts)
server.register_function(list_hostsconfig)
server.register_function(list_hoststemplate)
server.register_function(list_services)
server.register_function(list_servicestemplate)
server.register_function(agent_alive)
server.register_function(sync_conf)
server.register_function(restart_monitoring)

#### *****************************
#Faire une fonction save qui va faire une demande de recup des infos de la DB pour reecriture du fichier (cf la conf)
#Faire une fonction de push des fichier avant reecriture vers le serveur pour depot et suivi de version via SVN
#### *****************************

try:
	print 'Use Control-C to exit'
	#### *****************************
	## Send information to Inman master to declare the agent
	## Il faut un process independant pour la partie alive
	#### *****************************
	p = Process(target=agent_alive)
	p.start()
	server.serve_forever()
except KeyboardInterrupt:
	print 'Exiting'