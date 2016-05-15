#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import im_agentconfigclass_freeradius
import json
import logging
import os
import setproctitle
import redis
import time
import urllib2

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

def convertUserForRedis(collection_data, collection):
	logging.debug('Convert User for Redis'.format())
	to_redis = {}

	for collection_row in collection_data[collection]:
		collection_row = collection_row[0]
		if '{0}:{1}'.format(collection, collection_row['username']) in to_redis:
			logging.debug('User {0} already know. Add new right {1}'.format(collection_row['username'], collection_row['right']))
			to_redis['{0}:{1}'.format(collection, collection_row['username'])]['rights'].append(collection_row['right'])
		elif '{0}:{1}'.format(collection, collection_row['username']) not in to_redis:
			logging.debug('Prepare new user {} to be insert in Redis. Right {}'.format(collection_row['username'], collection_row['right']))
			to_redis['{0}:{1}'.format(collection, collection_row['username'])] = {'rights':[collection_row['right']], 'isldap': collection_row['isldap'], 'password': collection_row['password']}

	return to_redis

def hashfile(filename):
	hash = hashlib.md5()
	with open(filename, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash.update(chunk)
	return hash.digest()

def convertClientForRedis(collection_data, collection, to_redis):
	global ManageClientFile

	logging.debug('Convert Client for Redis'.format())

	flag_restart = False
	flag = False
	keys = []

	if to_redis:
		logging.debug('Vendor previously converted'.format())
		flag = True
		keys = to_redis.keys()

	checksum_before = hashfile('/etc/freeradius/clients_im.conf')

	for collection_row in collection_data[collection]:	
		collection_row = collection_row[0]

		if collection_row['sharedsecret'] != '':
			ManageClientFile.add_block(collection_row)

		logging.debug('Data to convert {0}'.format(collection_row))
		if flag:
			## Si la conversion Vendor est faite avant client
			logging.debug('Collection : {}, NAS IP : {}, Data : {}'.format(collection, collection_row['ip'], to_redis[collection_row['vendorname']]))
			to_redis['{0}:{1}'.format(collection, collection_row['ip'])] = to_redis[collection_row['vendorname']]
		else:
			logging.debug('Collection : {}, NAS IP : {}, Data : {}'.format(collection, collection_row['ip'], collection_row['vendorname']))
			to_redis['{0}:{1}'.format(collection, collection_row['ip'])] = collection_row['vendorname']

	for key in keys:
		del to_redis[key]

	logging.debug('Block to be insert in client_im : {}'.format(ManageClientFile.get_blocks()))
	ManageClientFile.commit_blocks()

	checksum_after = hashfile('/etc/freeradius/clients_im.conf')

	if checksum_before != checksum_after:
		logging.debug('Request to restart Freeradius'.format())
		ManageClientFile.restart_freeradius()

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

	for key in keys:
		del to_redis[key]

	return to_redis

def convertRangeForRedis(collection_data, collection):
	global ManageClientRangeFile

	to_redis = {}

	try:
		logging.debug('Convert Range for Redis'.format())
		for collection_row in collection_data[collection]:
			collection_row = collection_row[0]
			logging.debug('Prepare new range {} to be insert in Redis. Subnet {}'.format(collection_row['rangename'], collection_row['subnet']))
			to_redis['{0}:{1}'.format(collection, collection_row['rangename'])] = {'rangename': collection_row['rangename'], 'subnet': collection_row['subnet'], 'sharedsecret': collection_row['sharedsecret']}

			ManageClientRangeFile.add_block(collection_row)

		logging.debug('Block to be insert in client_im_range : {}'.format(ManageClientRangeFile.get_blocks()))
		ManageClientRangeFile.commit_blocks()
		logging.debug('Request to restart Freeradius'.format())
		ManageClientRangeFile.restart_freeradius()
		
	except Exception, e:
		logging.warning('Failed to convert Range for Redis -> {}'.format(e))
	
	return to_redis

def convertCollectionData(collection_data, collection2Sync):
	logging.debug('Convert data {0} from {1}'.format(collection_data, collection2Sync))

	to_redis = {}

	for collection in collection_data.keys():
		if collection == 'users_freeradius':
			to_redis = convertUserForRedis(collection_data, collection)
		elif collection == 'client_freeradius':
			to_redis = convertClientForRedis(collection_data, collection, to_redis)
		elif collection == 'vendor_freeradius':
			to_redis = convertVendorForRedis(collection_data, collection, to_redis)
		elif collection == 'range_freeradius':
			to_redis = convertRangeForRedis(collection_data, collection)
		
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

	try:
		headers = {'Content-Type': 'application/json'}
		query_args = {'agent_name': Conf.agent_name, 'collection2Sync': collection2Sync}
		data = json.dumps(query_args)

		url_sync_conf = 'http://'+Conf.inman_server+'/syncconf_freeradius'

		logging.debug('Launch sync conf for {0} from {1} : Get {2}'.format(Conf.agent_name, Conf.inman_server, collection2Sync))
		# Send HTTP POST request
		request_sync_conf = urllib2.Request(url_sync_conf, data, headers)
		response = urllib2.urlopen(request_sync_conf)
		collection_data = json.loads(response.read())

		logging.debug('Data get for {0} from {1} : Get {2}'.format(Conf.agent_name, Conf.inman_server, collection_data))

		logging.debug('Success sync conf for {0} from {1} : Get {2}'.format(Conf.agent_name, Conf.inman_server, collection2Sync))

		collection_data = convertCollectionData(collection_data, collection2Sync)

		saveToRedis(collection_data, collection2Sync)
	except Exception, e:
		logging.error('Failed sync conf for {0} from {1} : Get {2} -> {3}'.format(Conf.agent_name, Conf.inman_server, collection2Sync, e))
		raise e

def agent_alive():
	logging.debug('Agent {0} confirm to {1} is alive'.format(Conf.agent_name, Conf.inman_server))
	return True

##**********************##
## MAIN                 ##
##**********************##

setproctitle.setproctitle('IM Agent Freeradius')

try:
	
	Conf = im_agentconfigclass_freeradius.ConfObjClass('im_agent_freeradius.cfg', 'im_agent_freeradius_confcheck.cfg')
	
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
