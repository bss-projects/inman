#! /usr/bin/env python
#
# Python module file for INMAN management plugin
#
#

import json
import radiusd
import redis
import MySQLdb as mdb

#####################
# List of info inside Request
# 'User-Name'
# 'Reply-Message'
# 'User-Password'
# 'NAS-Port'
# 'NAS-Port-Id'
# 'NAS-Port-Type'
# 'Calling-Station-Id'
# 'NAS-IP-Address'
# 'Event-Timestamp'
#####################


def get_radius_attribute(attribute, attributes):
	for attr, val in attributes:
		if attr==attribute:
			return val
	return None

def authenticate(p):

	d_user_info = None
	username = get_radius_attribute('User-Name', p)[1:-1].lower()
	password = get_radius_attribute('User-Password', p)[1:-1]
	user_station = get_radius_attribute('Calling-Station-Id', p)
	nas_ip = get_radius_attribute('NAS-IP-Address', p)

	RedisPool = redis.ConnectionPool()
	RedisDB = redis.Redis(connection_pool=RedisPool)

	d_user_info = RedisDB.get('users_freeradius:{0}'.format(username))

	RedisPool.disconnect()

	if d_user_info:
		d_user_info = json.loads(d_user_info)

	print
	print p
	print

	if d_user_info['password'] == password:
		radiusd.radlog(radiusd.L_AUTH, 'Authenticate User {0}@{1} on {2}'.format(username, user_station, nas_ip))
		return (radiusd.RLM_MODULE_OK)
	else:
		radiusd.radlog(radiusd.L_AUTH, 'Failed : Reject access for User {0}@{2} on {3}'.format(username, password, user_station, nas_ip))
		return (radiusd.RLM_MODULE_FAIL)

def authorize(p):

	try:
		attr = []
		d_user_info = None
		d_nas_info = None
		l_flag = None
		l_ret_attr = []

		username = get_radius_attribute('User-Name', p)[1:-1].lower()
		password = get_radius_attribute('User-Password', p)[1:-1]
		user_station = get_radius_attribute('Calling-Station-Id', p)
		nas_ip = get_radius_attribute('NAS-IP-Address', p)

		radiusd.radlog(radiusd.L_INFO, 'Authorize Request for {0}@{1} on {2}'.format(username, user_station, nas_ip))
		print
		print p
		print

		RedisPool = redis.ConnectionPool()
		RedisDB = redis.Redis(connection_pool=RedisPool)

		d_user_info = RedisDB.get('users_freeradius:{0}'.format(username))
		d_nas_info = RedisDB.get('client_freeradius:{0}'.format(nas_ip))

		RedisPool.disconnect()

		###
		# @ToDo Python switch case like 
		###

		if d_user_info == None:
			# Unknown User
			radiusd.radlog(radiusd.L_ERR, 'Unknown User {0} on this RADIUS'.format(username))
			return radiusd.RLM_MODULE_FAIL
		elif d_nas_info == None:
			# Unknown NAS
			radiusd.radlog(radiusd.L_ERR, 'Unknown NAS {0} on this RADIUS'.format(nas_ip))
			return radiusd.RLM_MODULE_FAIL
		elif d_user_info == None and d_nas_info == None :
			# Unknown NAS and User
			radiusd.radlog(radiusd.L_ERR, 'Unknown NAS {0} and User {1} on this RADIUS'.format(nas_ip, username))
			return radiusd.RLM_MODULE_FAIL

		d_user_info = json.loads(d_user_info)
		d_nas_info = json.loads(d_nas_info)

		for right in d_user_info['rights']:
			if right in d_nas_info:
				l_flag = d_nas_info[right]

		if l_flag == None:
			radiusd.radlog(radiusd.L_ERR, 'No rights found for {0} on {1}'.format(username, nas_ip))
			return radiusd.RLM_MODULE_FAIL

		for flag in l_flag:
			attr = [str(flag.keys()[0]),str(flag.values()[0])]
			l_ret_attr.append(tuple(attr))

		if d_user_info['isldap'] == 'true':
			auth_type = ['Auth-Type', 'LDAP']
		else:
			auth_type = ['Auth-Type', 'Python']

		radiusd.radlog(radiusd.L_INFO, 'Get Authorization for {0} on {1}'.format(username, nas_ip))
		radiusd.radlog(radiusd.L_INFO, 'Flag send for {0} on {1} : {2}'.format(username, nas_ip, tuple(l_ret_attr)))
		return (radiusd.RLM_MODULE_UPDATED,tuple(l_ret_attr), (tuple(auth_type),))

	except Exception, e:
		radiusd.radlog(radiusd.L_ERR, 'Authorize Request failed {0}'.format(e))
		return radiusd.RLM_MODULE_FAIL
