#! /usr/bin/env python
#
# Python module file for INMAN management plugin
# Cega - 2015
#
#

import json
import radiusd
import redis
import time

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

def ip_to_int(ip):
	o = map(int, ip.split('.'))
	res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
	return res

def authenticate(p):

	d_user_info = None
	char_to_strip = '\'\"'

	username = get_radius_attribute('User-Name', p).strip(char_to_strip).lower()
	password = get_radius_attribute('User-Password', p)
	password_strip = password.strip(char_to_strip)
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

	if d_user_info['password'] == password_strip or d_user_info['password'] == password:
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
		flag_in_perimeter = False
		l_flag = None
		l_ret_attr = []
		char_to_strip = '\'\"'

		username = get_radius_attribute('User-Name', p).strip(char_to_strip).lower()
		password = get_radius_attribute('User-Password', p)
		password_strip = password.strip(char_to_strip)
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

		if 'expiration_timestamp' in d_user_info.keys():
			if time.time() > d_user_info['expiration_timestamp'] + 86399 :
				radiusd.radlog(radiusd.L_ERR, 'User {0} account expired'.format(username))
				return radiusd.RLM_MODULE_FAIL

		for right in d_user_info['rights']:
			if right in d_nas_info:
				l_flag = d_nas_info[right]

		if l_flag == None:
			radiusd.radlog(radiusd.L_ERR, 'No rights found for {0} on {1}'.format(username, nas_ip))
			return radiusd.RLM_MODULE_FAIL

		for flag in l_flag:
			attr = [str(flag.keys()[0]),str(flag.values()[0])]
			l_ret_attr.append(tuple(attr))

		if 'network_perimeter_freeradius' in d_user_info :
			flag_in_perimeter = False
			for perimeter in d_user_info['network_perimeter_freeradius'] :
				if type(perimeter) is list :
					if nas_ip in perimeter :
						flag_in_perimeter = True
				if type(perimeter) is dict :
					if ip_to_int(nas_ip) >= ip_to_int(perimeter['first_ip']) and ip_to_int(nas_ip) <= ip_to_int(perimeter['last_ip']) :
						flag_in_perimeter = True

			if flag_in_perimeter == False :
				radiusd.radlog(radiusd.L_ERR, 'User {0} is limited on specific network perimeter. {1} out of perimeter'.format(username, nas_ip))
				return radiusd.RLM_MODULE_FAIL
			else :
				radiusd.radlog(radiusd.L_INFO, 'User {0} get right to reach {1} inside network perimeter'.format(username, nas_ip))

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

	if username  == '"toto"':
		info1 = ['Session-Timeout', str(5)]
		info2 = ['Service-Type', 'NAS-Prompt-User']
		info3 = ['cisco-avpair', '"shell:priv-lvl=15"']
		attr1 = ['', '']
		g_ret = [tuple(info1), tuple(info2), tuple(info3)]
		return (radiusd.RLM_MODULE_UPDATED,tuple(g_ret), (tuple(attr1),))
#		return (
#			radiusd.RLM_MODULE_UPDATED,
#			(
##				('Session-Timeout', str(10)),
#				('Service-Type', 'NAS-Prompt-User'),
#				('cisco-avpair', '"shell:priv-lvl=15"')
#			),
#			(
#				('', ''),
##				('Auth-Type', 'LDAP'),
#			)
#		)

	elif get_radius_attribute('User-Name', p) == '"test_admin"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Xylan-Asa-Access', 'all'),
				('Xylan-Acce-Priv-F-R1', '0xf007e000'),
				('Xylan-Acce-Priv-F-R2', '0x00000003')
#				('Xylan-Acce-Priv-F-R1', '0xf0000000'),
#				('Xylan-Acce-Priv-F-R2', '0x00000003')
			),
			(
				('', ''),
			)
		)


	elif get_radius_attribute('User-Name', p) == '"roInt_admin"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Xylan-Asa-Access', 'all'),
				('Xylan-Acce-Priv-F-R1', '0xf007e002'),
				('Xylan-Acce-Priv-F-R2', '0x00000003')
#				('Xylan-Acce-Priv-F-R1', '0xf0000000'),
#				('Xylan-Acce-Priv-F-R2', '0x00000003')
			),
			(
				('', ''),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"roAll_admin"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Xylan-Asa-Access', 'all'),
				('Xylan-Acce-Priv-F-R1', '0xffffffff'),
				('Xylan-Acce-Priv-F-R2', '0xffffffff')
			),
			(
				('', ''),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"rwInt_admin"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Xylan-Asa-Access', 'all'),
				('Xylan-Acce-Priv-F-R1', '0xffffffff'),
				('Xylan-Acce-Priv-F-R2', '0xffffffff'),
				('Xylan-Acce-Priv-F-W1', '0x30008000'),
				('Xylan-Acce-Priv-F-W2', '0x00000000')
			),
			(
				('', ''),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"rwAll_admin"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Xylan-Asa-Access', 'all'),
				('Xylan-Acce-Priv-F-R1', '0xffffffff'),
				('Xylan-Acce-Priv-F-R2', '0xffffffff'),
				('Xylan-Acce-Priv-F-W1', '0xffffffff'),
				('Xylan-Acce-Priv-F-W2', '0xffffffff')
			),
			(
				('', ''),
			)
		)

	elif get_radius_attribute('User-Name', p) == '"roInt_admin_hp"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'NAS-Prompt-User'),
				('HP-Command-Exception', '0'),
				('Hp-Command-String', 'show interfaces *;show vlan *;show log*;exit')
			),
			(
				('Auth-Type', 'Python'),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"roAll_admin_hp"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'NAS-Prompt-User'),
				('HP-Command-Exception', '1'),
				('HP-Command-String', 'enable')
			),
			(
				('', ''),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"rwInt_admin_hp"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'Administrative-User'),
				('HP-Command-Exception', '0'),
				('Hp-Command-String', 'show *;configure terminal;interface *;enable;disable;speed-duplex *;vlan *;name *;untagged *;port-security *;spanning-tree *;exit')
			),
			(
				('', ''),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"rwAll_admin_hp"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'Administrative-User'),
				('HP-Command-Exception', '1')
			#	('Hp-Command-String', '*')
			),
			(
				('', ''),
			)
		)

	elif get_radius_attribute('User-Name', p) == '"roInt_admin_cisco"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'NAS-Prompt-User'),
				('cisco-avpair', '"shell:priv-lvl=1"')
			),
			(
				('', ''),
			)
		)

	elif get_radius_attribute('User-Name', p) == '"roAll_admin_cisco"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'NAS-Prompt-User'),
				('cisco-avpair', '"shell:priv-lvl=5"')
			),
			(
				('', ''),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"rwInt_admin_cisco"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'NAS-Prompt-User'),
				('cisco-avpair', '"shell:priv-lvl=10"')
			),
			(
				('', ''),
			)
		)
	elif get_radius_attribute('User-Name', p) == '"rwAll_admin_cisco"':
		return (
			radiusd.RLM_MODULE_UPDATED,
			(
				('Service-Type', 'NAS-Prompt-User'),
				('cisco-avpair', '"shell:priv-lvl=15"')
			),
			(
				('', ''),
			)
		)
	else:
		return radiusd.RLM_MODULE_FAIL
