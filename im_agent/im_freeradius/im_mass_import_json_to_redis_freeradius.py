#!/usr/bin/python
# -*- coding: utf-8 -*-

####
## import redis ready json formated file import_client_redis.json like
###
## {'client_freeradius:172.28.250.102': {u'exploit_niv1': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}, {u'Timetra-Cmd': u'show;info;configure port;
##admin save'}, {u'Timetra-Action': u'permit'}], u'exploit_niv2': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Default-Action': u'permit-all'}, {u'Timetra-Cmd': u'configure router;
## monitor router'}, {u'Timetra-Action': u'deny'}], u'exploit_niv3': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Default-Action': u'permit-all'}, {u'Timetra-Cmd': u''}, {u'Timetra
##-Action': u''}], u'support_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}, {u'Timetra-Cmd': u'show;info;'}, {u'Timetra-Action': u'permit'}
##], u'etude_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}, {u'Timetra-Cmd': u'configure port info; show port'}, {u'Timetra-Action': u'perm
##it'}]}, 'client_freeradius:172.28.253.116': {u'exploit_niv1': [{u'Vendor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-R2': u'0xFFFFFFFF'}, {u'Xy
##lan-Acce-Priv-F-W1': u'0x0000B00F'}, {u'Xylan-Acce-Priv-F-W2': u'0x00000000'}], u'exploit_niv2': [{u'Vendor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0xFFFFFFFF'}, {u'Xylan-Acc
##e-Priv-F-R2': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-W1': u'0xf005ffe9'}, {u'Xylan-Acce-Priv-F-W2': u'0x10010ff3'}], u'exploit_niv3': [{u'Vendor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-Priv-
##F-R1': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-R2': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-W1': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-W2': u'0xffffffff'}], u'etude_projet': [{u'Vendor code': u'800'}, {u'Xylan-Asa-Ac
##cess': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0x00008000'}, {u'Xylan-Acce-Priv-F-R2': u'0x00000000'}, {u'Xylan-Acce-Priv-F-W1': u'0x00000002'}, {u'Xylan-Acce-Priv-F-W2': u'0x00000000'}], u'support_projet': [{u'V
##endor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-R2': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-W1': u'0x00000002'}, {u'Xylan-Acce-Priv-F-W2': u'0x
##00000000'}]}, 'client_freeradius:172.28.253.21': {u'exploit_niv1': [{u'Vendor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-R2': u'0xFFFFFFFF'}, 
##{u'Xylan-Acce-Priv-F-W1': u'0x0000B00F'}, {u'Xylan-Acce-Priv-F-W2': u'0x00000000'}], u'exploit_niv2': [{u'Vendor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0xFFFFFFFF'}, {u'Xyla
##n-Acce-Priv-F-R2': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-W1': u'0xf005ffe9'}, {u'Xylan-Acce-Priv-F-W2': u'0x10010ff3'}], u'exploit_niv3': [{u'Vendor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-
##Priv-F-R1': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-R2': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-W1': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-W2': u'0xffffffff'}], u'etude_projet': [{u'Vendor code': u'800'}, {u'Xylan-A
##sa-Access': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0x00008000'}, {u'Xylan-Acce-Priv-F-R2': u'0x00000000'}, {u'Xylan-Acce-Priv-F-W1': u'0x00000002'}, {u'Xylan-Acce-Priv-F-W2': u'0x00000000'}], u'support_projet': 
##[{u'Vendor code': u'800'}, {u'Xylan-Asa-Access': u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-R2': u'0xFFFFFFFF'}, {u'Xylan-Acce-Priv-F-W1': u'0x00000002'}, {u'Xylan-Acce-Priv-F-W2':
## u'0x00000000'}]}, 'client_freeradius:172.28.252.69': {u'exploit_niv3': [{u'Service-Type': u'NAS-Prompt-User'}, {u'cisco-avpair': u'shell:priv-lvl=15'}, {u'Reply-Message': u''}]}, 'client_freeradius:172.28.252
##.68': {u'exploit_niv3': [{u'Service-Type': u'NAS-Prompt-User'}, {u'cisco-avpair': u'shell:priv-lvl=15'}, {u'Reply-Message': u''}]}, 'client_freeradius:172.28.253.102': {u'exploit_niv3': [{u'Xylan-Asa-Access': 
##u'all'}, {u'Xylan-Acce-Priv-F-R1': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-R2': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-W1': u'0xffffffff'}, {u'Xylan-Acce-Priv-F-W2': u'0xffffffff'}]}, 'client_freeradius:1.1.1.1': {
##u'droit_x': [{u'attribut1': u'all'}, {u'attribut2': u'*'}]}, 'client_freeradius:172.28.250.236': {u'etude_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action'
##: u'deny-all'}, {u'Timetra-Cmd': u'configure port info; show port'}, {u'Timetra-Action': u'permit'}], u'exploit_niv2': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Default-Action
##': u'permit-all'}, {u'Timetra-Cmd': u'configure router; monitor router'}, {u'Timetra-Action': u'deny'}], u'exploit_niv3': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Default-Act
##ion': u'permit-all'}, {u'Timetra-Cmd': u''}, {u'Timetra-Action': u''}], u'exploit_niv1': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}, {u'Timetra
##-Cmd': u'show;info;configure port;admin save;'}, {u'Timetra-Action': u'permit'}], u'support_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}
##, {u'Timetra-Cmd': u'show;info;'}, {u'Timetra-Action': u'permit'}]}, 'client_freeradius:172.28.250.235': {u'etude_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default
##-Action': u'deny-all'}, {u'Timetra-Cmd': u'configure port info; show port'}, {u'Timetra-Action': u'permit'}], u'exploit_niv2': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Defaul
##t-Action': u'permit-all'}, {u'Timetra-Cmd': u'configure router; monitor router'}, {u'Timetra-Action': u'deny'}], u'exploit_niv3': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Def
##ault-Action': u'permit-all'}, {u'Timetra-Cmd': u''}, {u'Timetra-Action': u''}], u'exploit_niv1': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}, {u
##'Timetra-Cmd': u'show;info;configure port;admin save;'}, {u'Timetra-Action': u'permit'}], u'support_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'de
##ny-all'}, {u'Timetra-Cmd': u'show;info;'}, {u'Timetra-Action': u'permit'}]}, 'client_freeradius:172.28.250.109': {u'support_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timet
##ra-Default-Action': u'deny-all'}, {u'Timetra-Cmd': u'show;info;'}, {u'Timetra-Action': u'permit'}], u'exploit_niv2': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Default-Action':
## u'permit-all'}, {u'Timetra-Cmd': u'configure router; monitor router'}, {u'Timetra-Action': u'deny'}], u'exploit_niv3': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both'}, {u'Timetra-Default-Actio
##n': u'permit-all'}, {u'Timetra-Cmd': u''}, {u'Timetra-Action': u''}], u'etude_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}, {u'Timetra-C
##md': u'configure port info; show port'}, {u'Timetra-Action': u'permit'}], u'exploit_niv1': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-all'}, {u'Timet
##ra-Cmd': u'show;info;configure port;admin save;'}, {u'Timetra-Action': u'permit'}]}, 'client_freeradius:172.28.250.108': {u'exploit_niv1': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u
##'Timetra-Default-Action': u'deny-all'}, {u'Timetra-Cmd': u'show;info;configure port;admin save'}, {u'Timetra-Action': u'permit'}], u'exploit_niv2': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'both
##'}, {u'Timetra-Default-Action': u'permit-all'}, {u'Timetra-Cmd': u'configure router; monitor router'}, {u'Timetra-Action': u'deny'}], u'exploit_niv3': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'b
##oth'}, {u'Timetra-Default-Action': u'permit-all'}, {u'Timetra-Cmd': u''}, {u'Timetra-Action': u''}], u'support_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Ac
##tion': u'deny-all'}, {u'Timetra-Cmd': u'show;info;'}, {u'Timetra-Action': u'permit'}], u'etude_projet': [{u'Vendor Alcatel-IPD': u'6527'}, {u'Timetra-Access': u'console'}, {u'Timetra-Default-Action': u'deny-al
##l'}, {u'Timetra-Cmd': u'configure port info; show port'}, {u'Timetra-Action': u'permit'}]}, 'client_freeradius:172.28.250.12': {u'exploit_niv1': [{u'Sam-security-group-name': u'Exploitant_SAM_N1'}], u'exploit_
##niv2': [{u'Sam-security-group-name': u'Exploitant_SAM_N2'}], u'exploit_niv3': [{u'Sam-security-group-name': u'Exploitant_SAM_N3'}], u'etude_projet': [{u'Sam-security-group-name': u'Etude_SAM_Project'}], u'supp
##ort_projet': [{u'Sam-security-group-name': u'Support_SAM_Project'}]}, ...
####

import ast
import json
import redis
import setproctitle
import sys
import traceback

def saveToRedis(collection_data):
	global RedisPool

	print 'Save data to Redis'.format()
	
	try:
		RedisDB = redis.Redis(connection_pool=RedisPool)
		pipeBulkToInsert = RedisDB.pipeline()

		if collection_data :
			for key in collection_data.keys():
				print 'Inserted data to Redis {0} -> {1}'.format(key, json.dumps(collection_data[key]))
				pipeBulkToInsert.set(key, json.dumps(collection_data[key]))

			pipeBulkToInsert.execute()
	except Exception, e:
		print '-- saveToRedis --\n Failed to save data to Redis -> {0}\n Error stack : {1}\n'.format(e, traceback.format_exc())
		raise e

	return

##**********************##
## MAIN                 ##
##**********************##

setproctitle.setproctitle('IM REDIS JSON Mass import')

try:
	RedisPool = redis.ConnectionPool()

	dict_file = sys.argv[1]
	
	with open(dict_file, 'r') as fd:
		dict_string = fd.read()
		dict_to_import = ast.literal_eval(dict_string)
		print dict_to_import
		print type(dict_to_import)

	saveToRedis(dict_to_import)

except Exception, e:
	print '-- MAIN --\n Failed to process Redis import -> {0}\n Error stack : {1}\n'.format(e, traceback.format_exc())
	raise e