#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import json
import logging
import os
import setproctitle
import redis
import time
import traceback
import urllib2

from im_agentconfigclass_freeradius import ConfObjClass, ManageCluster
from im_clientfileconfigclass_freeradius import ParseConfRadiusClient
from multiprocessing import Process, Queue
from pprint import pprint
from SimpleXMLRPCServer import SimpleXMLRPCServer

def master_alive():
	try:
		global Conf

		pid = os.getpid()

		fd = open('/var/run/im/im_agent_alive_freeradius.pid', 'w')
		fd.write(str(pid))
		fd.close()

		flag = 0 #le contact a eu lieu remise a 0 qd contact perdu

		headers = {'Content-Type': 'application/json'}

		query_args = {'agent_hostname': Conf.agent_hostname, 'agent_name': Conf.agent_name, 'agent_ip': Conf.agent_ip, 'agent_connection_type': Conf.agent_connection_type, 'agent_rpc_port': Conf.agent_rpc_port, 'plugin': 'freeradius'}

		data = json.dumps(query_args)

		url_register = 'http://'+Conf.inman_server+'/register_agent_freeradius'
		url_alive = 'http://'+Conf.inman_server+'/im_masteralive_freeradius'

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

def attach_user_to_network_perimeter(l_user_network_perimeter, to_redis):
	t_ret = []

	for user_network_perimeter in l_user_network_perimeter:
		info_network_perimeter = to_redis['{0}:{1}'.format('network_perimeter_freeradius', user_network_perimeter['uid'])]

		if info_network_perimeter['perimeter_type'] == 'subnet':
			t_ret.append({'first_ip': info_network_perimeter['first_ip'], 'last_ip': info_network_perimeter['last_ip']})
		else:
			t_ret.append(info_network_perimeter['ip_list'])

	return t_ret

def convertUserForRedis(collection_data, collection, to_redis):
	logging.debug('Convert User for Redis'.format())

	flag_perimeter = False
	keys = to_redis.keys()

	if 'network_perimeter_freeradius' in keys:
		logging.debug('Network Perimeter previously converted'.format())
		flag_perimeter = True

	to_redis['users_freeradius'] = []

	for collection_row in collection_data[collection]:
		collection_row = collection_row[0]
		if '{0}:{1}'.format(collection, collection_row['username']) in to_redis:
			logging.debug('User {0} already know. Add new right {1}'.format(collection_row['username'], collection_row['right']))
			to_redis['{0}:{1}'.format(collection, collection_row['username'])]['rights'].append(collection_row['right'])
		elif '{0}:{1}'.format(collection, collection_row['username']) not in to_redis:
			logging.debug('Prepare new user {0} to be insert in Redis. Right {1}'.format(collection_row['username'], collection_row['right']))
			to_redis['{0}:{1}'.format(collection, collection_row['username'])] = {'rights':[collection_row['right']], 'isldap': collection_row['isldap'], 'password': collection_row['password'], 'expiration_timestamp': collection_row['expiration_timestamp']}
			if flag_perimeter and ('network_perimeter' in collection_row):
				logging.debug('Attach {0} to his network perimeter data'.format(collection_row['username']))
				to_redis['{0}:{1}'.format(collection, collection_row['username'])]['network_perimeter_freeradius'] = attach_user_to_network_perimeter(collection_row['network_perimeter'], to_redis)
			elif flag_perimeter == False and ('network_perimeter' in collection_row):
				to_redis['{0}:{1}'.format(collection, collection_row['username'])]['network_perimeter_freeradius'] = collection_row['network_perimeter']
				to_redis['users_freeradius'].append('{0}:{1}'.format(collection, collection_row['username']))

	if 	to_redis['users_freeradius'] == []:
		del to_redis['users_freeradius']

	if flag_perimeter :
		for key in to_redis['network_perimeter_freeradius']:
			del to_redis[key]
		del to_redis['network_perimeter_freeradius']

	logging.debug('USER Data converted : {0}'.format(to_redis))

	return to_redis

def convertNetworkPerimeterForRedis(collection_data, collection, to_redis):
	logging.debug('Convert Network Perimeter for Redis'.format())

	flag_user = False
	keys = to_redis.keys()

	if 'users_freeradius' in keys:
		logging.debug('User previously converted before Network Perimeter'.format())
		flag_user = True

	to_redis['network_perimeter_freeradius'] = []

	logging.debug('List row from Network Perimeter for Redis {0}'.format(collection_data[collection]))
	for collection_row in collection_data[collection]:
		logging.debug('Get row from Network Perimeter : {0}'.format(collection_row))

		collection_row_data = collection_row[0]
		logging.debug('Collection Row data : {0}'.format(collection_row))
		collection_row_id = collection_row[1]
		logging.debug('Collection Row ID : {0}'.format(collection_row_id))

		logging.debug('Prepare new perimeter {0} -> Perimeter ID :{1}'.format(collection_row_data['label'], collection_row_id))
		
		if collection_row_data['perimeter_type'] == 'subnet':
			collection_row_data['ip_list'] = None
		else:
			collection_row_data['first_ip'] = None
			collection_row_data['last_ip'] = None

		to_redis['{0}:{1}'.format(collection, collection_row_id)] = {'perimeter_label': collection_row_data['label'], 'perimeter_type': collection_row_data['perimeter_type'], 'first_ip': collection_row_data['first_ip'], 'last_ip': collection_row_data['last_ip'], 'ip_list': collection_row_data['ip_list']}
		to_redis['network_perimeter_freeradius'].append('{0}:{1}'.format(collection, collection_row_id))

	if to_redis['network_perimeter_freeradius'] == []:
		del to_redis['network_perimeter_freeradius']

	if flag_user:
		logging.debug('List user previously insert to attach network perimeter'.format())
		for user in to_redis['users_freeradius']:
			logging.debug('Attach {0} previously insert with network perimeter data'.format(user))
			to_redis[user]['network_perimeter_freeradius'] = attach_user_to_network_perimeter(to_redis[user]['network_perimeter_freeradius'], to_redis)

		for key in to_redis['network_perimeter_freeradius']:
			del to_redis[key]
		del to_redis['users_freeradius']
		del to_redis['network_perimeter_freeradius']

	logging.debug('NETWORK PERIMETER Data converted : {0}'.format(to_redis))

	return to_redis

def hashfile(filename):
	hash = hashlib.md5()
	with open(filename, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash.update(chunk)
	return hash.digest()

def convertClientForRedis(collection_data, collection, to_redis):
###	global ManageClientFile

	logging.debug('Convert Client for Redis'.format())

	flag_restart = False
	flag = False
	keys = []

	if to_redis:
		logging.debug('Vendor previously converted'.format())
		flag = True
		keys = to_redis.keys()

###	checksum_before = hashfile('/etc/freeradius/clients_im.conf')

	for collection_row in collection_data[collection]:	
		collection_row = collection_row[0]

###		if 'sharedsecret' not in collection_row:
###			collection_row['sharedsecret'] = ''

###		if collection_row['sharedsecret'] != '':
###			ManageClientFile.add_block(collection_row)

		logging.debug('Data to convert {0}'.format(collection_row))
		if flag:
			## Si la conversion Vendor est faite avant client
			logging.debug('Collection : {0}, NAS IP : {1}, Data : {2}'.format(collection, collection_row['ip'], to_redis[collection_row['vendorname']]))
			to_redis['{0}:{1}'.format(collection, collection_row['ip'])] = to_redis[collection_row['vendorname']]
		else:
			logging.debug('Collection : {0}, NAS IP : {1}, Data : {2}'.format(collection, collection_row['ip'], collection_row['vendorname']))
			to_redis['{0}:{1}'.format(collection, collection_row['ip'])] = collection_row['vendorname']

	##~~
	# This part is just to have less information insert in REDIS.
	# We try to insert only the minimum information need for rlm_python
	# So we delete temp info
	# Soon this part won't be necessary because we will get our information
	# directly into preformated view
	##~~
	####
	#for key in keys:
	#	del to_redis[key]
	####

###	logging.debug('Block to be insert in client_im : {0}'.format(ManageClientFile.get_blocks()))
###	ManageClientFile.commit_blocks()

###	checksum_after = hashfile('/etc/freeradius/clients_im.conf')

###	if checksum_before != checksum_after:
###		logging.debug('Request to restart Freeradius'.format())
###		ManageClientFile.restart_freeradius()

	logging.debug('CLIENT Data converted : {0}'.format(to_redis))

	return to_redis

def getRightLevel(vendorname, l_flag_level):
	logging.debug('Get right level for {0} in {1}'.format(vendorname, l_flag_level))
	ret = {}

	for level in l_flag_level:
		if level['label'] != 'list_flag':
			ret[level['label']] = level['l_flag']

	logging.debug('Right level for {0} -> {1}'.format(vendorname, ret))
	return ret

def convertVendorForRedis(collection_data, collection, to_redis):
	logging.debug('Convert Vendor for Redis'.format())

	flag = False
	keys = []

	if to_redis:
		flag = True
		keys = to_redis.keys()

	for collection_row in collection_data[collection]:
		collection_row = collection_row[0]
		logging.debug('Data to convert {0}'.format(collection_row))
		if flag:
			## Si la conversion Client est faite avant vendor
			for key, val in to_redis.items():
				if collection_row['vendorname'] == val:
					to_redis[key] = getRightLevel(collection_row['vendorname'], collection_row['l_flag_level'])
		else:
			to_redis[collection_row['vendorname']] = getRightLevel(collection_row['vendorname'], collection_row['l_flag_level'])

	##~~
	# This part is just to have less information insert in REDIS.
	# We try to insert only the minimum information need for rlm_python
	# So we delete temp info
	# Soon this part won't be necessary because we will get our information
	# directly into preformated view
	##~~
	####
	# if not flag:
	#	for key in keys:
	#		del to_redis[key]
	####

	logging.debug('VENDOR Data converted : {0}'.format(to_redis))

	return to_redis

def convertIPInBinary(ip_cidr_string):
	ip_cidr_bin = 0
	ip, cidr = ip_cidr_string.split('/')

	cidr_binary = bin(int(cidr))[3:]
	ip_binary = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
	ip_cidr_bin = int('{0}{1}'.format(ip_binary, cidr_binary))

	return ip_cidr_bin

def orderRangeByIP(d_range):
	ip_cidr_bin = 0
	l_range_order = []
	d_ipbin_rangedate = {}

	try:
		logging.debug('Order Range'.format())

		for range_data in d_range:
			range_data = range_data[0]
			ip_cidr_bin = convertIPInBinary(range_data['subnet'])
			d_ipbin_rangedate[ip_cidr_bin] = range_data

		l_range_order = sorted(d_ipbin_rangedate, reverse=True)

		return l_range_order, d_ipbin_rangedate
	except Exception, e:
		logging.error('Failed to order range -> {0}'.format(e))
		raise e
	


def convertRangeForRedis(collection_data, collection, to_redis):
	global ManageClientRangeFile

#	to_redis = {}
	l_range_order = []

	try:
		logging.debug('Convert Range for Redis'.format())
		l_range_order, collection_sorted = orderRangeByIP(collection_data[collection])
		for index in l_range_order:
#			collection_row = collection_row[0]
			collection_row = collection_sorted[index]
			logging.debug('Prepare new range {0} to be insert. Subnet {1}'.format(collection_row['rangename'], collection_row['subnet']))
			to_redis['{0}:{1}'.format(collection, collection_row['rangename'])] = {'rangename': collection_row['rangename'], 'subnet': collection_row['subnet'], 'sharedsecret': collection_row['sharedsecret']}

			ManageClientRangeFile.add_block(collection_row)

		logging.debug('Block to be insert in client_im_range : {0}'.format(ManageClientRangeFile.get_blocks()))
		ManageClientRangeFile.commit_blocks()
		logging.debug('Request to restart Freeradius'.format())
		ManageClientRangeFile.restart_freeradius()
		
	except Exception, e:
		logging.warning('Failed to convert Range for Redis -> {0}'.format(e))
	
	logging.debug('RANGE Data converted : {0}'.format(to_redis))

	return to_redis

def convertSharedsecretForRedis(collection_data, collection, to_redis):
	global ManageClientFile

#	to_redis = {}

	try:
		logging.debug('Convert Shared secret for Redis'.format())
		checksum_before = hashfile('/etc/freeradius/clients_im.conf')

		for collection_row in collection_data[collection]:
			collection_row = collection_row[0]
			logging.debug('Prepare new shared secret {0} to be insert. IP {1}'.format(collection_row['name'], collection_row['ip']))
			to_redis['{0}:{1}'.format(collection, collection_row['name'])] = {'name': collection_row['name'], 'ip': collection_row['ip'], 'sharedsecret': collection_row['sharedsecret']}

			ManageClientFile.add_block(collection_row)

		logging.debug('Block to be insert in client_im : {0}'.format(ManageClientFile.get_blocks()))
		ManageClientFile.commit_blocks()

		checksum_after = hashfile('/etc/freeradius/clients_im.conf')

		if checksum_before != checksum_after:
			logging.debug('Request to restart Freeradius'.format())
			ManageClientFile.restart_freeradius()
		
	except Exception, e:
		logging.warning('Failed to convert Shared secret for Redis -> {0}'.format(e))
	
	logging.debug('SHARED KEY CLIENT Data converted : {0}'.format(to_redis))

	return to_redis

def convertCollectionData(collection_data, collection2Sync):
	logging.debug('Convert data {0} from {1}'.format(collection_data, collection2Sync))

	to_redis = {}

	for collection in collection_data.keys():
		if collection == 'users_freeradius':
			to_redis = convertUserForRedis(collection_data, collection, to_redis)
		elif collection == 'network_perimeter_freeradius':
			to_redis = convertNetworkPerimeterForRedis(collection_data, collection, to_redis)
		elif collection == 'client_freeradius':
			to_redis = convertClientForRedis(collection_data, collection, to_redis)
		elif collection == 'vendor_freeradius':
			to_redis = convertVendorForRedis(collection_data, collection, to_redis)
		elif collection == 'range_freeradius':
			to_redis = convertRangeForRedis(collection_data, collection, to_redis)
		elif collection == 'shared_secret_freeradius':
			to_redis = convertSharedsecretForRedis(collection_data, collection, to_redis)
		
	logging.debug('Data converted {0}'.format(to_redis))
	return to_redis

def saveToRedis(collection_data,collection2Sync):
	global RedisPool

	to_delete = ''

	logging.debug('Save data to Redis'.format())
	
	try:
		RedisDB = redis.Redis(connection_pool=RedisPool)
		pipeBulkToInsert = RedisDB.pipeline()
		for collection_info in collection2Sync:
			collection = collection_info['collection']
			logging.debug('Flush collection {0} before save in Redis'.format(collection))
			list_keys = RedisDB.keys('{0}*'.format(collection))
			logging.debug('List of keys delete in {0} : {1}'.format(collection, list_keys))
			if list_keys:
				RedisDB.delete(*list_keys)

		if collection_data :
			for key in collection_data.keys():
				logging.debug('Inserted data to Redis {0} -> {1}'.format(key, json.dumps(collection_data[key])))
				pipeBulkToInsert.set(key, json.dumps(collection_data[key]))

			pipeBulkToInsert.execute()
	except Exception, e:
		logging.error('Failed to save data to Redis -> {0}'.format(e))
		raise e

	return

def sync_conf(collection2Sync):
	global Conf
	global RedisPool

	try:
		headers = {'Content-Type': 'application/json'}
		query_args = {'agent_name': Conf.agent_name, 'collection2Sync': collection2Sync}
		data = json.dumps(query_args)

		url_sync_conf = 'http://'+Conf.inman_server+'/syncconf_freeradius'

		logging.debug('Launch sync conf for {0} from {1} : Get {2}'.format(Conf.agent_name, Conf.inman_server, collection2Sync))
		# Send HTTP POST request
		request_sync_conf = urllib2.Request(url_sync_conf, data, headers)
		logging.debug('Request URL "{0}" with data {1}'.format(url_sync_conf, data))
		response = urllib2.urlopen(request_sync_conf)
		logging.debug('Response return for URL "{0}" with data {1} -> {2}'.format(url_sync_conf, data, response))
		collection_data = json.loads(response.read())

		logging.debug('Data get for {0} from {1} : Get {2}'.format(Conf.agent_name, Conf.inman_server, collection_data))

		logging.debug('Success sync conf for {0} from {1} : Get {2}'.format(Conf.agent_name, Conf.inman_server, collection2Sync))

		collection_data = convertCollectionData(collection_data, collection2Sync)

		saveToRedis(collection_data, collection2Sync)
		###
		cluster_group = ManageCluster(RedisPool, logging)
		cluster_group.launch_nodes_sync()
		###
	except Exception, e:
		logging.error('Failed sync conf for {0} from {1} : Get {2} -> {3} URL = {4}\n {5}'.format(Conf.agent_name, Conf.inman_server, collection2Sync, e, url_sync_conf, traceback.format_exc()))
		raise e

def agent_alive():
	logging.debug('Agent {0} confirm to {1} is alive'.format(Conf.agent_name, Conf.inman_server))
	return True

def register_cluster_node(d_cluster_node):
	try:
		collection_data = {'cluster_node:{0}'.format(d_cluster_node['hostname']): d_cluster_node['info']}
		saveToRedis(collection_data,[])
		logging.info('Register cluster node {0} on {1}'.format(d_cluster_node['hostname'], Conf.agent_name))
		return True, 'Register cluster node {0} on {1}'.format(d_cluster_node['hostname'], Conf.agent_name)
	except Exception, e:
		logging.error('Failed to register {0} on {1} : {2}'.format(d_cluster_node['hostname'], Conf.agent_name, e))
		return False, 'Failed to register {0} on {1}'.format(d_cluster_node['hostname'], Conf.agent_name)

##**********************##
## MAIN                 ##
##**********************##

setproctitle.setproctitle('IM Agent Freeradius')

try:
	
	Conf = ConfObjClass('im_agent_freeradius.cfg', 'im_agent_freeradius_confcheck.cfg')
	
	if not os.path.isfile(Conf.log_file):
		path, filename = os.path.split(Conf.log_file)
		os.makedirs(path)
		open(Conf.log_file, 'a').close()
	
	logging.basicConfig(level=eval(Conf.log_debug_level), filename=Conf.log_file, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

	ManageClientFile = ParseConfRadiusClient("clients_im.conf", Conf.client_filepath)
	ManageClientRangeFile = ParseConfRadiusClient("clients_im_range.conf", Conf.client_filepath)

	RedisPool = redis.ConnectionPool()

	server = SimpleXMLRPCServer(('0.0.0.0', Conf.agent_rpc_port), logRequests=True, allow_none=True)

	server.register_function(agent_alive)
	server.register_function(master_alive)
	server.register_function(sync_conf)
	server.register_function(register_cluster_node)
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
