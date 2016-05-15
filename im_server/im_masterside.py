#!/usr/bin/python
# -*- coding: utf-8 -*-

import bottle as inman
import cgi
import gc
import gettext
import json
import logging
import os.path
import pprint
import pycas
import re
import setproctitle
import time
import xmlrpclib

from beaker.middleware import SessionMiddleware
from bottle import Bottle, route, run, template, request, response, static_file, redirect
from im_agentdialogclass import ClassAgent, ClassAgentFreeradius
from im_dbclass import DBManagement, DBManagement_postgres
from jinja2 import Environment, FileSystemLoader, Template
from os import listdir
from os.path import isfile, join

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': True,
	'session.timeout': 28800,
	'session.data_dir': './web_session',
	'session.auto': True
}

CAS_SERVER  = 'https://cas-server.lan:443/websso'
SERVICE_URL = 'http://inman.lan/cas_login'



if not os.path.isfile('/var/log/inman/im.log'):
	path, filename = os.path.split('/var/log/inman/im.log')
	os.makedirs(path)
	open('/var/log/inman/im.log', 'a').close()


# create logger
logger = logging.getLogger('inman')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.FileHandler('/var/log/inman/im.log')
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(fmt='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

#inman = Bottle()

try:
	logger.info('Initialize Inman server env'.format())
	setproctitle.setproctitle('IM Master')
	IMDB = DBManagement(database='inman')
	IMDB_psg = DBManagement_postgres()
	app = inman.default_app()
	app = SessionMiddleware(app, session_opts)

	t = gettext.translation('inman', 'translation', ['fr'], fallback=False)
	_ = t.ugettext
	env = Environment(loader=FileSystemLoader('./templates'), extensions=['jinja2.ext.i18n'])
	env.install_gettext_translations(t)
	l_templates = env.list_templates(extensions=['tpl'])
	
except Exception, e:
	logger.info('Failed to initialize Inman server : {0}'.format(e))
	raise e



@inman.route('/web/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='../web/')

def jsonp(request, dictionary):
	if (request.query.callback):
		return "%s(%s)" % (request.query.callback, json.dumps(dictionary))
	return json.dumps(dictionary)

@inman.post('/gettypehosticon')
@inman.get('/gettypehosticon')
def getTypeHostIcon():
	response.content_type = 'application/json'
	mypath = '../web/img/type_host'
	res = []

	for f in listdir(mypath):
		if isfile(join(mypath,f)):
			if re.search(request.query.get('q'), os.path.splitext(f)[0], re.IGNORECASE) is not None:
				res.append({'id': os.path.splitext(f)[0], 'text': os.path.splitext(f)[0], 'icon': join(mypath,f)[3:]})

	return jsonp(request, res)

def getAgentList4Type(agent_type):
	l_agent = []

	d_search_options = {\
		'query' :\
		{\
			'filtered' :\
			{ \
				'query' :\
				{\
					'match_all' : {} \
				},\
				'filter' : \
				{\
					'term' : \
					{ \
						'agent_connection_type': agent_type\
					}\
				}\
			}\
		}\
	}

	l_agent_res = IMDB.search(collection='agent_list', search_parameter=d_search_options)	

	for agent_res in l_agent_res:
		l_agent.append(agent_res['_source'])

	return l_agent

def getAgentList(supervisor='all'):
	l_agent = []

###
# @ToDo Par defaut la fonction renvois tous les superviseurs mais s'il sagit d'une requete
# avec un user en param alors on renvois juste les superviseurs pour ce user
###

	if supervisor == 'all':
		d_search_options = {\
			'query' :\
			{\
				'filtered' :\
				{ \
					'query' :\
					{\
						'match_all' : {} \
					},\
				}\
			}\
		}
	else:
		d_search_options = {\
			'query' :\
			{\
				'filtered' :\
				{ \
					'query' :\
					{\
						'match_all' : {} \
					},\
					'filter' : \
					{\
						'term' : \
						{ \
							'agent_alias': supervisor.lower()\
						}\
					}\
				}\
			}\
		}

	l_agent_res = IMDB.search(collection='agent_list', search_parameter=d_search_options)	

	for agent_res in l_agent_res:
		l_agent.append(agent_res['_source'])

	return l_agent

def isAgentInUpdate(db_collection_name, agent_alias):
	in_update = 0

	d_search_options = {\
		'query' :\
		{\
			'filtered' :\
			{ \
				'filter' : \
				{\
					'term' : \
					{ \
						'agent_alias': agent_alias.lower()\
					}\
				}\
			}\
		}\
	}

	l_agent = IMDB.search(collection=db_collection_name, search_parameter=d_search_options)	

	for agent in l_agent:
		if 'in_update' in agent:
			in_update = agent['_source']['in_update']

	return in_update

def getOidInDB(db_collection_name, agent_alias, idKey=None):
	oid = None

####
# @ Todo faire la fonction qui recup la liste des superviseur granted et les mettre dans le tab des term
####

	if idKey == None:
		d_search_options = {\
			"query" :\
			{\
				"filtered" :\
				{ \
					"filter" : \
					{\
						"term" : \
						{ \
							"agent_alias": agent_alias.lower()\
						}\
					}\
				}\
			}\
		}
	else:
		d_search_options = {\
			'query' :\
			{\
				'filtered' :\
				{ \
					'filter' : \
					{\
						'bool' :\
						{\
							'must' :\
							[\
								{'term' : \
								{ \
									'agent_alias': agent_alias.lower()\
								}},\
								{'term' : \
								{ \
									db_collection_name: idKey.lower()\
								}}\
							]\
						}\
					}\
				}\
			}\
		}

	l_results = IMDB.search(collection=db_collection_name, search_parameter=d_search_options)

	if len(l_results) == 0:
		print '#############'
		pprint.pprint(idKey)
		print '#############'

	for result in l_results:
		oid = result['_id']

	return oid

def define_tunnel_port(d_agent_info):
	l_port = []
	port_ssh_tunnel = 0
	i = 0

	l_agent = getAgentList4Type('SSH')

	for agent in l_agent:
		if agent_info['agent_alias'] == d_agent_info['agent_alias']:
			return agent_info['port_ssh_tunnel']
		l_port.append(agent_info['port_ssh_tunnel'])

	while True:
		i += 1
		port_ssh_tunnel = d_agent_info['agent_rpc_port'] + i
		if port_ssh_tunnel not in l_port:
			return port_ssh_tunnel

def insertConfInDB(db_collection_name, agent_alias, l_confInfo):
	oid = None

	for key, confInfo in l_confInfo.items():
		confEntry = {'agent_alias': agent_alias, db_collection_name: key, key: confInfo}

		oid = getOidInDB(db_collection_name, agent_alias, key)

		if oid is not None:
			IMDB.update(collection=db_collection_name, doc=confEntry, id=oid)
		else:
			res = IMDB.publish(collection=db_collection_name, doc=confEntry)
			IMDB.publish(collection=db_collection_name+'_ref', doc={'agent_alias': agent_alias, db_collection_name: key, 'oid': res['_id']})












#################################################
### *********************************************
### FREERADIUS Master Part
### *********************************************
#################################################




def import_file_csv_data_client_freeradius(path_file):
	
	doc = {}
	important_type = ['"radiusname"', '"name"', '"shortname"', '"ip"', '"vendorname"', '"sharedsecret"']
	place_important_type = []
	header = []
	l_file_data = []
	tmp = {}
	i = 0

	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = ''

	try:
		flag_column_header = 0
		fd = open(path_file, 'r')

		for line in fd:
			if not flag_column_header:
				header = line.split(';')
				c = 0
				for ctype in header:
					if ctype in important_type:
						place_important_type.append(c)
					c += 1
				flag_column_header = 1
			else:
				l_line = line.split(';')
				for place in place_important_type:
					tmp[header[place].strip('\"')] = l_line[place].strip('\"')

				l_file_data.append(json.dumps(tmp.copy()).replace('\'', '\'\''))

				i += 1

		doc['client_info'] = l_file_data

		IMDB_psg.multi_publish(collection='client_freeradius', doc=doc)
	
		response.status = '202 '+_('Save in database')
		res.append(_('Save in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Save failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.post('/upload_freeradius')
def upload_freeradius():
	fileupload = request.files['files[]']
	fileupload.save('../web/fileupload/freeradius', overwrite=True)
	return (import_file_csv_data_client_freeradius('../web/fileupload/freeradius/{0}'.format(fileupload.filename)))

def getDocInDB_freeradius(uid, db_collection_name, doc_field_name):
	l_results = []
	d_search_options = {}

	d_search_options['fields'] = doc_field_name
	d_search_options['filter'] = 'id = \''+ str(uid) +'\''

	l_results = IMDB_psg.search(collection=db_collection_name, search_parameter=d_search_options)

	return l_results[0][0]

@inman.post('/im_get_doc_freeradius')
@inman.get('/im_get_doc_freeradius')
def A_getDoc_freeradius():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[], 'doc': {}}
	oldID = None

	##Fonction qui liste les agent_alias authorise en fonction du user et donc font la liste des OR pour le AND

	uid = request.query.get('uid')
	collection = request.query.get('collection')
	fields = request.query.get('fields')

	doc = getDocInDB_freeradius(uid, collection, fields)

	val_ret['doc'] = doc.copy()

	return jsonp(request, val_ret)

@inman.post('/im_get_vendor_Toedit_freeradius')
@inman.get('/im_get_vendor_Toedit_freeradius')
def A_getVendorToEdit_freeradius():
	d_search_options = {}
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[], 'data': ''}
	res = []

	collection = request.query.get('collection')
	vendorToedit = request.query.get('vendortoedit')
	radiusname = request.query.get('radius')
	uid = request.query.get('uid')

	d_search_options['filter'] = 'id = \''+ uid +'\''
	d_search_options['fields'] = 'vendor_info'

	try:
		ret = IMDB_psg.search(collection, d_search_options)
		response.status = '202 '+_('Select in database')
		res.append(_('Select in database'))
		val_ret["results"] = res
		l_flag_level = ret[0][0]['l_flag_level']
		for flag_level in l_flag_level:
			if flag_level['label'] == 'list_flag':
				l_block = flag_level['l_block']
				for block in l_block:
					block_title = block['block_name']
					val_ret['data'] += '<div class="info_frame info_frame-dismissable col-lg-12"> \
											<h4>'+block_title.encode('utf-8')+'</h4>  \
											<button class="close" aria-hidden="true" type="button" data-dismiss="alert">×</button> \
											<div class="list_flag col-lg-12">'
										
					for att in block['list']:
						val_ret['data'] += '	<div class="entry_list_flag col-lg-12"> \
													<div class="col-lg-11">'+ att.keys()[0].encode('utf-8') +'</div> \
													<div class="col-lg-1"> \
														<i class="fa fa-trash-o fake-link remove_flag"></i> \
													</div> \
												</div>'


					val_ret['data'] +='		</div>\
											<div class="input-group col-lg-12">\
												<input type="flag_name_freeradius" class="form-control flag_name" name="flag_name_freeradius" placeholder="Nom de l\'attribut"> \
												<span class="input-group-btn"> \
													<button class="btn btn-default add_flag" type="button"> \
														<i class="fa fa-plus"></i> \
														Ajout nouvel attribut \
													</button> \
												</span> \
											</div>\
										</div>'

				break
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Select failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.post('/im_delete_right_freeradius')
@inman.get('/im_delete_right_freeradius')
def A_deleteRightInDB_freeradius():
	doc = {}
	d_search_options = {}
	l_flag_level = []
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	collection = request.query.get('collection')
	vendorname = request.query.get('vendorname')
	label = request.query.get('label')
	radiusname = request.query.get('radius')
	uid = request.query.get('uid')


	d_search_options['filter'] = 'id = \''+ str(uid) +'\''
	d_search_options['fields'] = 'vendor_info'

	ret = IMDB_psg.search(collection='vendor_freeradius', search_parameter=d_search_options)

	to_insert = ret[0][0]

	for flag_level in to_insert['l_flag_level']:
		if flag_level['label'] != label:
			l_flag_level.append(flag_level)

	to_insert['l_flag_level'] = l_flag_level
	to_insert = json.dumps(to_insert).replace('\'', '\'\'')

	doc['vendor_info'] = to_insert

	try:
		ret = IMDB_psg.update(collection='vendor_freeradius', doc=doc, search_parameter=d_search_options)
		response.status = '202 '+_('Delete in database')
		res.append(_('Delete in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Delete failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.post('/im_delete_entry_freeradius')
@inman.get('/im_delete_entry_freeradius')
def A_deleteEntryInDB_freeradius():
	d_search_options = {}
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	collection = request.query.get('collection')
	vendorTodelete = request.query.get('vendortodelete')
	radiusname = request.query.get('radius')
	uid = request.query.get('uid')

	d_search_options['filter'] = 'id = \''+ uid +'\''

	try:
		IMDB_psg.delete(collection, uid, d_search_options)
		response.status = '202 '+_('Delete in database')
		res.append(_('Delete in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Delete failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

def getList_freeradius(db_collection_name, plugin='all', user='all', filter=None, fields='*'):
	i = 0
	ret = []
	l_results = []
	d_search_options = {}
	d_search_options['filter'] = ''

	l_dbname_info = db_collection_name.split('_')
	if l_dbname_info[0] == 'users':
		l_dbname_info[0] = 'user'

	l_agent = getAgentList_freeradius(plugin=plugin)
	length = len(l_agent)

	for agent in l_agent:
		i += 1
		if  length > i:
			d_search_options['filter'] += '{0}_info->>\'radiusname\' = \'{1}\' OR '.format(l_dbname_info[0], agent['agent_name'])
		else :
			d_search_options['filter'] += '{0}_info->>\'radiusname\' = \'{1}\''.format(l_dbname_info[0], agent['agent_name'])

	if length == 0:
		d_search_options['filter'] = filter

	d_search_options['plugin'] = plugin
	d_search_options['user'] = user
	d_search_options['fields'] = fields

	l_results = IMDB_psg.search(collection=db_collection_name, search_parameter=d_search_options)

	return l_results

def getRightList_freeradius(plugin='all', user='all'):

	d_search_options = {}
	l_right = []
###
# @ToDo Par defaut la fonction renvois tous les agent mais s'il sagit d'une requete
# avec un user en param alors on renvois juste les superviseurs pour ce user
###

	d_search_options['plugin'] = plugin
	d_search_options['user'] = user
	d_search_options['view'] = 'list_right'

	if plugin != 'all':
		d_search_options['view'] = d_search_options['view']+'_'+plugin

	d_search_options['fields'] = 'view_data'
	d_search_options['filter'] = 'name = \''+ d_search_options['view'] +'\''

	l_right_res = IMDB_psg.search(collection='matview', search_parameter=d_search_options)	

	for right in l_right_res[0][0]:
		l_right.append({'right' : right})

	return l_right

def getVendorList_freeradius(plugin='all', user='all'):

	d_search_options = {}
	l_vendor = []
###
# @ToDo Par defaut la fonction renvois tous les agent mais s'il sagit d'une requete
# avec un user en param alors on renvois juste les superviseurs pour ce user
###

	d_search_options['plugin'] = plugin
	d_search_options['user'] = user
	d_search_options['view'] = 'list_vendor'

	if plugin != 'all':
		d_search_options['view'] = d_search_options['view']+'_'+plugin

	d_search_options['fields'] = 'view_data'
	d_search_options['filter'] = 'name = \''+ d_search_options['view'] +'\''

	l_vendor_res = IMDB_psg.search(collection='matview', search_parameter=d_search_options)	

	for vendor in l_vendor_res[0][0]:
		l_vendor.append({'vendorname' : vendor})

	return l_vendor

def getVendorFlagList_freeradius(plugin='all', user='all'):

	d_search_options = {}
	l_flag_vendor = []
###
# @ToDo Par defaut la fonction renvois tous les agent mais s'il sagit d'une requete
# avec un user en param alors on renvois juste les superviseurs pour ce user
###

	d_search_options['plugin'] = plugin
	d_search_options['user'] = user
	d_search_options['view'] = 'list_flag_vendor'

	if plugin != 'all':
		d_search_options['view'] = d_search_options['view']+'_'+plugin

	d_search_options['fields'] = 'view_data'
	d_search_options['filter'] = 'name = \''+ d_search_options['view'] +'\''

	l_flag_vendor_res = IMDB_psg.search(collection='matview', search_parameter=d_search_options)	

	if l_flag_vendor_res:
		for flag_vendor in l_flag_vendor_res[0][0]:
			l_flag_vendor.append(flag_vendor)

	return l_flag_vendor


def getAgentList_freeradius(plugin='all', user='all'):

	l_agent = []
	s = inman.request.environ.get('beaker.session')

	rights = s['rights']['rights']

	for right in rights:
		if right['plugin_name'] == plugin:
			for agent in right['agent']:
				l_agent.append({'agent_name' : agent})

	return l_agent


@inman.post('/im_getlistinfo_freeradius/<data>/<cat>/<radiusname>')
@inman.get('/im_getlistinfo_freeradius/<data>/<cat>/<radiusname>')
def A_getListInfo_freeradius(data, cat, radiusname='all'):
	
	l_label = []
	response.content_type = 'application/json'
	val_ret = {'draw': 10, 'recordsTotal': 0, 'recordsFiltered': 10, 'data': []}
	res = {}
	recordsTotal = 0
	type_list = {}

	type_list['vendor_freeradius-vendor'] = {}
	type_list['vendor_freeradius-vendor']['fields'] = 'id, json_build_object(\'radiusname\', vendor_info->\'radiusname\', \'vendorname\', vendor_info->\'vendorname\')'
	type_list['vendor_freeradius-vendor']['columns'] = {'radiusname': 'radius', 'vendorname': 'vendeur'}

	type_list['vendor_freeradius-right'] = {}
	type_list['vendor_freeradius-right']['fields'] = 'id, json_build_object(\'radiusname\', vendor_info->\'radiusname\', \'vendorname\', vendor_info->\'vendorname\', \'label\', vendor_info->\'l_flag_level\')'
	type_list['vendor_freeradius-right']['columns'] = {'radiusname': 'radius', 'vendorname': 'vendeur', 'label': 'label'}

	type_list['client_freeradius-client'] = {}
	type_list['client_freeradius-client']['fields'] = 'id, json_build_object(\'radiusname\', client_info->\'radiusname\', \'vendorname\', client_info->\'vendorname\', \'ip\', client_info->\'ip\', \'client\', client_info->\'name\')'
	type_list['client_freeradius-client']['columns'] = {'radiusname': 'radius', 'vendorname': 'vendeur', 'ip': 'ip', 'client': 'client'}

	type_list['users_freeradius-user'] = {}
	type_list['users_freeradius-user']['fields'] = 'id, json_build_object(\'radiusname\', user_info->\'radiusname\', \'username\', user_info->\'username\', \'right\', user_info->\'right\', \'isldap\', user_info->\'isldap\')'
	type_list['users_freeradius-user']['columns'] = {'radiusname': 'radius', 'username': 'utilisateur', 'right': 'droit', 'isldap': 'connexion'}

	type_list['range_freeradius-range'] = {}
	type_list['range_freeradius-range']['fields'] = 'id, json_build_object(\'radiusname\', range_info->\'radiusname\', \'rangename\', range_info->\'rangename\', \'subnet\', range_info->\'subnet\')'
	type_list['range_freeradius-range']['columns'] = {'radiusname': 'radius', 'rangename': 'nom', 'subnet': 'sous-reseau'}

	##Fonction qui liste les host info authorise en fonction du user et donc font la liste des OR pour le AND

	l_info = getList_freeradius(data, plugin='freeradius', filter=radiusname, fields=type_list[data+'-'+cat]['fields'])

	for info in l_info:
		recordsTotal += 1
		uid = info[0]
		row = info[1]
		dataTableColumns = row.keys()
		action = '<div class="btn-group btn-group-xs">\
					<input class="uid" type="hidden" value="'+ str(uid) +'" />\
					<button type="button" name="btn_delete" data-container="body" data-toggle="tooltip" data-placement="left" title="'+_('Delete '+cat)+'" class="btn btn-default btn_delete_'+cat+'"><i class="fa fa-trash-o"></i></button>\
					<button type="button" name="btn_edit" data-container="body" data-toggle="tooltip" data-placement="right" title="'+_('Edit '+cat)+'" class="btn btn-default btn_edit_'+cat+'"><i class="fa fa-edit"></i></button>\
				</div>'

		if cat == 'vendor' or cat == 'client' or cat == 'range':
			for column in dataTableColumns:
				res[type_list[data+'-'+cat]['columns'][column]] = row[column]

		elif cat == 'user':
			for column in dataTableColumns:
				if column == 'isldap':
					if row[column] == 'true':
						res[type_list[data+'-'+cat]['columns'][column]] = 'LDAP'
					else:
						res[type_list[data+'-'+cat]['columns'][column]] = 'Local'
				else:
					res[type_list[data+'-'+cat]['columns'][column]] = row[column]

		elif cat == 'right':
			for column in dataTableColumns:
				if column != 'label':
					res[type_list[data+'-'+cat]['columns'][column]] = row[column]
				elif column == 'label':
					recordsTotal -= 1
					for flag_level in row[column]:
						if flag_level['label'] != 'list_flag':
							recordsTotal += 1
							l_label.append(flag_level['label'])

		res['action'] = action
		if l_label != [] and cat == 'right':
			for label in l_label:
				res['label'] = label
				val_ret['data'].append(res.copy())
		elif cat == 'vendor' or cat == 'client' or cat == 'user' or cat == 'range':
			val_ret['data'].append(res.copy())
		res = {}
		l_label = []

	val_ret['recordsTotal'] = recordsTotal
 
	return jsonp(request, val_ret)

def getVendorFlagValueList_freeradius(uid, label, collection):
	d_search_options = {}
	l_vendor_flag_value = []
###
# @ToDo Par defaut la fonction renvois tous les agent mais s'il sagit d'une requete
# avec un user en param alors on renvois juste les superviseurs pour ce user
###

	d_search_options['fields'] = 'json_build_object(\'radiusname\', vendor_info->\'radiusname\', \'vendorname\', vendor_info->\'vendorname\', \'l_flag_level\', vendor_info->\'l_flag_level\')'
	d_search_options['filter'] = 'id = \''+ uid +'\''

	l_row = IMDB_psg.search(collection=collection, search_parameter=d_search_options)	

	for flag_level in l_row[0][0]['l_flag_level']:
		if flag_level['label'] == label:
			return flag_level['l_flag']

@inman.post('/im_list_flag_value_vendor_freeradius')
@inman.get('/im_list_flag_value_vendor_freeradius')
def A_getListFlagValueVendor_freeradius():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[], 'data': ''}
	res = []
	ret = {}
	oldID = None

	##Fonction qui liste les agent_alias authorise en fonction du user et donc font la liste des OR pour le AND

	vendorname = request.query.get('vendorname')
	radiusname = request.query.get('radiusname')
	label = request.query.get('label')
	uid = request.query.get('uid')

	l_flag = getVendorFlagValueList_freeradius(uid, label, 'vendor_freeradius')
	for flag in l_flag:
		flag_name = flag.keys()[0]
		flag_val = flag[flag_name]
		val_ret['data'] += '<div class="input-group col-lg-12"> \
								<div class="input-group"> \
									<span class="input-group-addon">'+flag_name+'</span> \
									<input class="form-control" type="text" value="'+flag_val.replace('"', '&quot;')+'"> \
								</div> \
							</div>'

	return jsonp(request, val_ret)

@inman.post('/im_list_flag_vendor_freeradius')
@inman.get('/im_list_flag_vendor_freeradius')
def A_getListFlagVendor_freeradius():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[], 'data': ''}
	res = []
	ret = {}
	oldID = None

	##Fonction qui liste les agent_alias authorise en fonction du user et donc font la liste des OR pour le AND

	vendorname = request.query.get('vendorname')

	l_result = getVendorFlagList_freeradius(plugin='freeradius')
	for result in l_result:
		# Rajout dans le IF du fait que le superviseur soit dans liste de droit du user ou pas
		if result['vendorname'] == vendorname:
			for flag in result['l_flag']:
				flag = flag.keys()[0]
				val_ret['data'] += '<div class="input-group"> \
										<div class="input-group"> \
											<span class="input-group-addon">'+ flag +'</span> \
											<input class="form-control" type="text" placeholder="'+_('Value')+'"> \
										</div> \
									</div>'

	return jsonp(request, val_ret)


@inman.post('/im_list_right_autocomplete_freeradius')
@inman.get('/im_list_right_autocomplete_freeradius')
def A_getListRight_4autocomplete_freeradius():
	ret = []

	l_result = getRightList_freeradius(plugin='freeradius')

	for result in l_result:
		ret.append(result['right'])

	return json.dumps(ret)

@inman.post('/im_list_right_freeradius')
@inman.get('/im_list_right_freeradius')
def A_getListRight_freeradius():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}
	oldID = None

	##Fonction qui liste les agent_alias authorise en fonction du user et donc font la liste des OR pour le AND

	l_result = getRightList_freeradius(plugin='freeradius')
	for result in l_result:
		# Rajout dans le IF du fait que le superviseur soit dans liste de droit du user ou pas
		if re.search(request.query.get('q'), result['right'], re.IGNORECASE) is not None and oldID != result['right']:
			res.append({'id': result['right'], 'text': result['right']})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/im_list_vendor_freeradius')
@inman.get('/im_list_vendor_freeradius')
def A_getListVendor_freeradius():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}
	oldID = None

	##Fonction qui liste les agent_alias authorise en fonction du user et donc font la liste des OR pour le AND

	l_result = getVendorList_freeradius(plugin='freeradius')
	for result in l_result:
		# Rajout dans le IF du fait que le superviseur soit dans liste de droit du user ou pas
		if re.search(request.query.get('q'), result['vendorname'], re.IGNORECASE) is not None and oldID != result['vendorname']:
			res.append({'id': result['vendorname'], 'text': result['vendorname']})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/im_list_agent_freeradius')
@inman.get('/im_list_agent_freeradius')
def A_getListAgent_freeradius():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}
	oldID = None

	l_result = getAgentList_freeradius(plugin='freeradius')
	for result in l_result:
		# Rajout dans le IF du fait que le superviseur soit dans liste de droit du user ou pas
		if re.search(request.query.get('q'), result['agent_name'], re.IGNORECASE) is not None and oldID != result['agent_name']:
			res.append({'id': result['agent_name'], 'text': result['agent_name']})

	val_ret["results"] = res

	return jsonp(request, val_ret)


@inman.get('/im_crud_user_freeradius/<action>')
def A_crud_user_freeradius(action):
	
	d_block = {}
	doc = {}
	d_flag_level = {}
	d_search_options = {}
	response.content_type = 'application/json'
	to_insert = {}
	val_ret = {"more": False, "results":[]}
	res = []
	ret = ''

	radiusname = request.query.get('radiusname')
	username = request.query.get('username')
	isldap = request.query.get('isldap')
	password = request.query.get('password')
	right = request.query.get('right')

	if username:
		to_insert['username'] = username.lower()
	to_insert['password'] = password
	to_insert['isldap'] = isldap
	to_insert['radiusname'] = radiusname
	to_insert['right'] = right
	to_insert = json.dumps(to_insert).replace('\'', '\'\'')

	doc['user_info'] = to_insert

	try:
		if action == 'new':
			ret = IMDB_psg.publish(collection='users_freeradius', doc=doc)
		elif action == 'edit' :
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.update(collection='users_freeradius', doc=doc, search_parameter=d_search_options)
		elif action == 'delete':
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.delete(collection='users_freeradius', id=uid, search_parameter=d_search_options)

		response.status = '202 '+_('Save in database')
		res.append(_('Save in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Save failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.get('/im_crud_client_freeradius/<action>')
def A_crud_client_freeradius(action):
	
	d_block = {}
	doc = {}
	d_flag_level = {}
	d_search_options = {}
	response.content_type = 'application/json'
	to_insert = {}
	val_ret = {"more": False, "results":[]}
	res = []
	ret = ''

	radiusname = request.query.get('radiusname')
	vendorname = request.query.get('vendorname')
	name = request.query.get('client')
	shortname = request.query.get('shortname')
	ip = request.query.get('ip')
	sharedsecret = request.query.get('sharedsecret')

	to_insert['name'] = name
	to_insert['ip'] = ip
	to_insert['vendorname'] = vendorname
	to_insert['shortname'] = shortname
	to_insert['sharedsecret'] = sharedsecret
	to_insert['radiusname'] = radiusname
	to_insert = json.dumps(to_insert).replace('\'', '\'\'')

	doc['client_info'] = to_insert

	try:
		if action == 'new':
			ret = IMDB_psg.publish(collection='client_freeradius', doc=doc)
		elif action == 'edit' :
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.update(collection='client_freeradius', doc=doc, search_parameter=d_search_options)
		elif action == 'delete':
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.delete(collection='client_freeradius', id=uid, search_parameter=d_search_options)

		response.status = '202 '+_('Save in database')
		res.append(_('Save in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Save failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.get('/im_crud_range_freeradius/<action>')
def A_crud_range_freeradius(action):
	
	d_block = {}
	doc = {}
	d_flag_level = {}
	d_search_options = {}
	response.content_type = 'application/json'
	to_insert = {}
	val_ret = {"more": False, "results":[]}
	res = []
	ret = ''

	radiusname = request.query.get('radiusname')
	rangename = request.query.get('rangename')
	subnet = request.query.get('subnet')
	sharedsecret = request.query.get('sharedsecret')

	to_insert['radiusname'] = radiusname
	to_insert['rangename'] = rangename
	to_insert['subnet'] = subnet
	to_insert['sharedsecret'] = sharedsecret
	to_insert = json.dumps(to_insert).replace('\'', '\'\'')

	doc['range_info'] = to_insert

	try:
		if action == 'new':
			ret = IMDB_psg.publish(collection='range_freeradius', doc=doc)
		elif action == 'edit' :
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.update(collection='range_freeradius', doc=doc, search_parameter=d_search_options)
		elif action == 'delete':
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.delete(collection='range_freeradius', id=uid, search_parameter=d_search_options)

		response.status = '202 '+_('Save in database')
		res.append(_('Save in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Save failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)


@inman.post('/im_crud_right_freeradius/<action>')
@inman.get('/im_crud_right_freeradius/<action>')
def A_crud_right_freeradius(action):
	
	d_block = {}
	doc = {}
	d_flag_level = {}
	d_search_options = {}
	response.content_type = 'application/json'
	to_insert = {}
	uid = None
	val_ret = {"more": False, "results":[]}
	res = []
	ret = ''

	d_flag = json.loads(request.query.get('l_flag'))
	radiusname = request.query.get('radiusname')
	vendorname = request.query.get('vendorname')
	label = request.query.get('label')

	d_flag_level['label'] = label
	d_flag_level['l_flag'] = []
	
	for flag in d_flag:
		d_flag_level['l_flag'].append(flag.copy())

	if action == 'new':
		d_search_options['filter'] = 'vendor_info->>\'vendorname\' = \''+ vendorname +'\' AND vendor_info->>\'radiusname\' = \''+ radiusname +'\''
	elif action == 'edit':
		uid = request.query.get('uid')
		d_search_options['filter'] = 'id = \''+ str(uid) +'\''

	d_search_options['fields'] = 'id, vendor_info'

	ret = IMDB_psg.search(collection='vendor_freeradius', search_parameter=d_search_options)

	if ret:
		uid = ret[0][0]
		to_insert = ret[0][1]
	else:
		d_search_options['filter'] = 'vendor_info->>\'vendorname\' = \''+ vendorname +'\''
		ret = IMDB_psg.search(collection='vendor_freeradius', search_parameter=d_search_options)
		to_insert = ret[0][1]
		to_insert['radiusname'] = radiusname
		l_flag_level = to_insert['l_flag_level']
		for flag_level in l_flag_level:
			if flag_level['label'] == 'list_flag':
				l_flag_level = [flag_level]
				break

	if action == 'new':
		to_insert['l_flag_level'].append(d_flag_level)
	elif action == 'edit':
		i = 0
		for level in to_insert['l_flag_level']:
			if level['label'] == label:
				print d_flag_level
				to_insert['l_flag_level'][i] = d_flag_level.copy()
			i += 1

	to_insert = json.dumps(to_insert).replace('\'', '\'\'')

	doc['vendor_info'] = to_insert

	try:
		if action == 'new':
			if uid:
				d_search_options['filter'] = 'id = \''+ str(uid) +'\''
				ret = IMDB_psg.update(collection='vendor_freeradius', doc=doc, search_parameter=d_search_options)
			else:
				ret = IMDB_psg.publish(collection='vendor_freeradius', doc=doc)
		elif action == 'edit' :
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.update(collection='vendor_freeradius', doc=doc, search_parameter=d_search_options)
		response.status = '202 '+_('Save in database')
		res.append(_('Save in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Save failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.post('/im_crud_vendor_freeradius/<action>')
@inman.get('/im_crud_vendor_freeradius/<action>')
def A_crud_vendor_freeradius(action):
	
	d_block = {}
	doc = {}
	d_flag_level = {}
	d_search_options = {}
	response.content_type = 'application/json'
	to_insert = {}
	val_ret = {"more": False, "results":[]}
	res = []
	ret = ''

	d_flag = json.loads(request.query.get('l_flag'))
	radiusname = request.query.get('radiusname')
	vendorname = request.query.get('vendorname')

	to_insert['radiusname'] = radiusname
	to_insert['vendorname'] = vendorname
	to_insert['l_flag_level'] = []
	d_flag_level['label'] = 'list_flag'
	d_flag_level['l_block'] = []
	
	l_block = d_flag.keys()

	for block in l_block:
		d_block['block_name'] = block
		d_block['list'] = []
		for att in d_flag[block]:
			d_block['list'].append({att:''})
		d_flag_level['l_block'].append(d_block.copy())

	to_insert['l_flag_level'].append(d_flag_level.copy())

	to_insert = json.dumps(to_insert).replace('\'', '\'\'')

	doc['vendor_info'] = to_insert

	try:
		if action == 'new':
			ret = IMDB_psg.publish(collection='vendor_freeradius', doc=doc)
		elif action == 'edit' :
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ uid +'\''
			ret = IMDB_psg.update(collection='vendor_freeradius', doc=doc, search_parameter=d_search_options)
		response.status = '202 '+_('Save in database')
		res.append(_('Save in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Save failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.post('/im_client_freeradius')
@inman.get('/im_client_freeradius')
def W_client_freeradius():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_client_freeradius.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_right_freeradius')
@inman.get('/im_right_freeradius')
def W_right_level_freeradius():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_right_freeradius.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_vendor_freeradius')
@inman.get('/im_vendor_freeradius')
def W_user_freeradius():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_vendor_freeradius.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_user_freeradius')
@inman.get('/im_user_freeradius')
def W_user_freeradius():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_user_freeradius.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_log_freeradius')
@inman.get('/im_log_freeradius')
def W_right_level_freeradius():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_log_freeradius.tpl')

	return OTemplate.render(d_render)

####
## Doit perdre le sufixe freeradius car commun tous les plugin
####
def getAgentListSSH_freeradius():
	l_agent = []
	d_search_options = {}
	l_results = []

	d_search_options['fields'] = 'json_build_object(\'agent_name\', agent_info->\'agent_name\', \'port_ssh_tunnel\', agent_info->\'port_ssh_tunnel\')'
	d_search_options['filter'] = 'CAST(agent_info->>\'port_ssh_tunnel\' AS INT) IS NOT NULL'

	l_results = IMDB_psg.search(collection='agent', search_parameter=d_search_options)

	return l_results

####
## Doit perdre le sufixe freeradius car commun tous les plugin
####
def define_tunnel_port_freeradius(d_agent_info):
	l_port = []
	port_ssh_tunnel = 0
	i = 0

	l_agent = getAgentListSSH_freeradius()

	for agent in l_agent:
		agent = agent[0]
		if agent['agent_name'] == d_agent_info['agent_name']:
			return agent['port_ssh_tunnel']
		l_port.append(agent['port_ssh_tunnel'])

	while True:
		i += 1
		port_ssh_tunnel = d_agent_info['agent_rpc_port'] + i
		if port_ssh_tunnel not in l_port:
			return port_ssh_tunnel

@inman.post('/register_agent_freeradius')
def A_register_agent_freeradius():

	uid = None
	doc = {}
	d_search_options = {}

	d_agent_info = request.json
	agent_name = d_agent_info['agent_name']

	try :
		if d_agent_info['agent_connection_type'] == 'SSH':
			port_ssh_tunnel = define_tunnel_port_freeradius(d_agent_info)
			d_agent_info['port_ssh_tunnel'] = port_ssh_tunnel

		to_insert = json.dumps(d_agent_info).replace('\'', '\'\'')
		doc['agent_info'] = to_insert
	
		d_search_options['filter'] = 'agent_info->>\'agent_name\' = \''+ agent_name +'\' AND agent_info->>\'plugin\' = \'freeradius\''
		d_search_options['fields'] = 'id, agent_info'
	
		ret = IMDB_psg.search(collection='agent', search_parameter=d_search_options)
	
		if ret :
			uid = ret[0][0]
	
		if uid is not None:
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.update(collection='agent', doc=doc, search_parameter=d_search_options)
		else:
			IMDB_psg.publish(collection='agent', doc=doc)

	except Exception, e:
		print e

####
## Cette fonction doit remplacer toutes les autres register agent
####
@inman.post('/register_agent_new')
def A_register_agent():

	logger.info('Register new agent : '.format())

	uid = None
	doc = {}
	d_search_options = {}

	d_agent_info = request.json
	agent_name = d_agent_info['agent_name']
	plugin = d_agent_info['plugin']

	logger.info('Name : {0}, Plugin : {1} '.format(agent_name, plugin))
	logger.debug('Agent info : {0}'.format(d_agent_info))

	try :
		if d_agent_info['agent_connection_type'] == 'SSH':
			logger.debug('Agent communicate RPC over SSH'.format())
			port_ssh_tunnel = define_tunnel_port_freeradius(d_agent_info)
			d_agent_info['port_ssh_tunnel'] = port_ssh_tunnel
			logger.debug('SSH port to bind with RPC : {0}'.format(port_ssh_tunnel))

		to_insert = json.dumps(d_agent_info).replace('\'', '\'\'')
		doc['agent_info'] = to_insert
	
		d_search_options['filter'] = 'agent_info->>\'agent_name\' = \'{0}\' AND agent_info->>\'plugin\' = \'{1}\''.format(agent_name, plugin)
		d_search_options['fields'] = 'id, agent_info'
	
		logger.debug('Is agent already in DB'.format())
		ret = IMDB_psg.search(collection='agent', search_parameter=d_search_options)
	
		if ret :
			uid = ret[0][0]
	
		if uid is not None:
			logger.debug('Yes UID in DB is : {0}'.format(uid))
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.update(collection='agent', doc=doc, search_parameter=d_search_options)
			logger.debug('Agent updated in DB'.format())
		else:
			logger.debug('No, Insert new agent in DB'.format())
			IMDB_psg.publish(collection='agent', doc=doc)

	except Exception, e:
		logger.error('Problem in agent registration : {0}'.format(e))

def searchDocInfo_freeradius(db_collection_name, d_search_options):
	l_results = []

	l_results = IMDB_psg.search(collection=db_collection_name, search_parameter=d_search_options)

	return l_results[0]

@inman.post('/launchsync_freeradius')
@inman.get('/launchsync_freeradius')
def A_launchSync_freeradius():

	countdown = 30
	d_search_options = {}
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	radiusname = request.query.get('radiusname')
	plugin = request.query.get('plugin')
	collection_info = json.loads(request.query.get('collection_info'))

	d_search_options['fields'] = '*'
	d_search_options['filter'] = 'agent_info->>\'agent_name\' = \'{0}\' AND agent_info->>\'plugin\' = \'{1}\''.format(radiusname, plugin)

	agent_doc = searchDocInfo_freeradius(db_collection_name='agent', d_search_options=d_search_options)
	d_agent_info = agent_doc[1]

	try:
		response.status = '202 '+_('Synchronization in progress')
		agent = ClassAgentFreeradius(d_agent_info, IMDB_psg)
		agent.connect()
		
		while True:
			time.sleep(1)
			if countdown == 0:
				print 'Agent {0} not available'.format(radiusname)
				break
			else:
				countdown -= 1

			try:
				if agent.agentalive():
					agent.initSync(collection_info)
				break
			except Exception, e:
				pass
				
		agent.close()
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		response.status = '444 '+_('Connection Failed')
		res.append(_('Synchronization failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		print e
		return jsonp(request, val_ret)

def getCollection_freeradius(db_collection, agent_name, json_field, json_key):
	d_search_options = {}

	try :

		logger.debug('Get data from collection "{}" : request field "{}_info" with filter "{}"'.format(db_collection, json_field, agent_name))
	
		d_search_options['filter'] = '{0}_info->>\'{1}\' = \'{2}\''.format(json_field, json_key, agent_name)
		d_search_options['fields'] = '{0}_info'.format(json_field)

		ret = IMDB_psg.search(collection=db_collection, search_parameter=d_search_options)

		logger.debug('Data retrieve from collection "{}" : {}'.format(db_collection, ret))	

		return ret
	except Exception, e:
		logger.debug('Failed to retrieve data from collection "{}" : {}'.format(db_collection, e))
		return None

@inman.post('/syncconf_freeradius')
@inman.get('/syncconf_freeradius')
def A_SyncConf_freeradius():

	data = None
	d_dataCollection = {}
	response.content_type = 'application/json'

	d_sync_info = request.json

	agent_name = d_sync_info['agent_name']
	l_db_collection = d_sync_info['collection2Sync']

	logger.debug('Request to get conf for RADIUS {} : {}'.format(agent_name, l_db_collection))

	for d_db_collection in l_db_collection:
		collection = d_db_collection['collection']
		json_field = d_db_collection['json_field']
		json_key = d_db_collection['json_key']

		logger.debug('Collection to get "{}" : Spec field to get "{}" ; Spec field to link "{}"'.format(collection, json_field, json_key))

		data = getCollection_freeradius(collection, agent_name, json_field, json_key)

		logger.debug('Data to sync for collection "{}" : {}'.format(collection, data))

		d_dataCollection[collection] = data

	return jsonp(request, d_dataCollection)

@inman.post('/im_masteralive_freeradius')
@inman.get('/im_masteralive_freeradius')
def A_master_alive_freeradius():

	return 'ok'

def isInmanUser(login, password=None):

	d_search_options = {}

	d_search_options['filter'] = 'user_info->>\'login\' = \''+ login.lower() +'\''
	d_search_options['fields'] = 'user_info'

	l_user_res = IMDB_psg.search(collection='users', search_parameter=d_search_options)

	if l_user_res:
		if password == None:
			return True
		elif password == l_user_res[0][0]['password']:
			return True

	return False

def verif_session():

	logger.debug('User session verification'.format())

	logger.debug('Get session info'.format())
	s = inman.request.environ.get('beaker.session')
	logger.debug('Session info : {0}'.format(s))

	if 'login' not in s:
		logger.debug('User not login. Redirect to SSO Login -> {0}'.format('/cas_login'))
		redirect('/cas_login')
	elif 'login' in s:
		if not isInmanUser(s['login']):
			logger.debug('User login OK. No Right on InMan. Redirect to ask access -> {0}'.format('/ask_registration'))
			redirect('/ask_registration')

	logger.debug('Session checked. Access granted'.format())
	return






#################################################
### *********************************************
### SUPERVISOR Master Part
### *********************************************
#################################################

@inman.post('/im_status_supervisor')
@inman.get('/im_status_supervisor')
def W_status_freeradius():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_status_supervisor.tpl')

	return OTemplate.render(d_render)



#################################################
### *********************************************
### ADMINISTRATION Master Part
### *********************************************
#################################################


@inman.post('/ask_registration')
@inman.get('/ask_registration')
def W_ask_registration():
	global env

	d_render = {'page_title': 'InMan - Configuration management tool'}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_ask_registration.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_get_user_Toedit')
@inman.get('/im_get_user_Toedit')
def A_getUserToEdit():
	d_search_options = {}
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[], 'data': ''}
	res = []

	collection = request.query.get('collection')
	login = request.query.get('login')
	uid = request.query.get('uid')

	d_search_options['filter'] = 'id = \''+ uid +'\''
	d_search_options['fields'] = 'user_info'

	try:
		ret = IMDB_psg.search(collection, d_search_options)
		response.status = '202 '+_('Select in database')
		res.append(_('Select in database'))
		val_ret["results"] = res

		l_rights = ret[0][0]['rights']

		for right in l_rights:
			plugin_name = right['plugin_name'].encode('utf-8')
			agents = ','.join(right['agent']).encode('utf-8')
			val_ret['data'] += '<tr> \
									<td> \
										<div class="info_frame info_frame-dismissable" class="col-sm-12"> \
											<h4>'+plugin_name+'</h4> \
											<button class="close" aria-hidden="true"type="button" data-dismiss="alert">×</button> \
											<div class="form-group"> \
												<label for="agent_user" class="col-sm-3 control-label">Agent</label> \
												<div class="col-sm-8"> \
													<input class="plugin_name" type="hidden" value="'+plugin_name+'"> \
													<input type="agent_user" class="form-control agent_user" id="agent_user" name="agent_user" placeholder="Agent" value="'+agents+'"> \
												</div> \
											</div> \
										</div> \
									</td> \
								</tr>'
										
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Select failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

@inman.get('/im_crud_user/<action>')
def A_crud_user(action):
	
	d_block = {}
	doc = {}
	d_flag_level = {}
	d_search_options = {}
	response.content_type = 'application/json'
	to_insert = {}
	val_ret = {"more": False, "results":[]}
	res = []
	ret = ''

	login = request.query.get('login')
	password = request.query.get('password')
	firstname = request.query.get('firstname')
	lastname = request.query.get('lastname')
	rights = request.query.get('rights')

	if action == 'new' or action == 'edit':
		to_insert['login'] = login.lower()
		to_insert['password'] = password
		to_insert['firstname'] = firstname
		to_insert['lastname'] = lastname
		to_insert['rights'] = json.loads(rights)
		to_insert = json.dumps(to_insert).replace('\'', '\'\'')

	doc['user_info'] = to_insert

	try:
		if action == 'new':
			ret = IMDB_psg.publish(collection='users', doc=doc)
		elif action == 'edit' :
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.update(collection='users', doc=doc, search_parameter=d_search_options)
		elif action == 'delete':
			uid = request.query.get('uid')
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''
			ret = IMDB_psg.delete(collection='users', id=uid, search_parameter=d_search_options)

		response.status = '202 '+_('Save in database')
		res.append(_('Save in database'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Save failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		return jsonp(request, val_ret)

def getAgentList(plugin='all', user='all'):

	d_search_options = {}
	l_agent = []
###
# @ToDo Par defaut la fonction renvois tous les agent mais s'il sagit d'une requete
# avec un user en param alors on renvois juste les superviseurs pour ce user
###

	d_search_options['user'] = user
	d_search_options['fields'] = 'agent_info'
	if plugin == 'all':
		d_search_options['filter'] = 'all'
	else:
		d_search_options['filter'] = 'agent_info->>\'plugin\' = \''+ plugin +'\''

	l_agent_res = IMDB_psg.search(collection='agent', search_parameter=d_search_options)

	for agent in l_agent_res:
		l_agent.append({'agent_name' : agent[0]['agent_name'], 'agent_ip' : agent[0]['agent_ip'], 'agent_connection_type' : agent[0]['agent_connection_type'], 'agent_hostname' : agent[0]['agent_hostname'], 'plugin_name' : agent[0]['plugin']})

	return l_agent

@inman.post('/im_getlistagentinfo/<plugin_name>')
@inman.get('/im_getlistagentinfo/<plugin_name>')
def A_getListAgentInfo(plugin_name):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	l_result = getAgentList(plugin=plugin_name)

	val_ret["results"] = l_result

	return jsonp(request, val_ret)

@inman.post('/im_getlistagent/<plugin_name>')
@inman.get('/im_getlistagent/<plugin_name>')
def A_getListAgent(plugin_name):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	l_result = getAgentList(plugin=plugin_name)
	for result in l_result:
		# Rajout dans le IF du fait que le superviseur soit dans liste de droit du user ou pas
		if re.search(request.query.get('q'), result['agent_name'], re.IGNORECASE) is not None:
			res.append({'id': result['agent_name'], 'text': result['agent_name']})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/im_getlist_user')
@inman.get('/im_getlist_user')
def A_getListUser():
	
	d_search_options = {}
	l_label = []
	plugin = ''
	response.content_type = 'application/json'
	val_ret = {'draw': 10, 'recordsTotal': 0, 'recordsFiltered': 10, 'data': []}
	res = {}
	recordsTotal = 0
	type_list = {}

	d_search_options['filter'] = 'all'
	d_search_options['fields'] = 'id, json_build_object(\'login\', user_info->\'login\', \'firstname\', user_info->\'firstname\', \'lastname\', user_info->\'lastname\', \'rights\', user_info->\'rights\')'
	d_search_options['columns'] = {'login': 'login', 'firstname': 'prenom', 'lastname': 'nom', 'plugin': 'plugin'}

	l_info = IMDB_psg.search(collection='users', search_parameter=d_search_options)

	for info in l_info:
		recordsTotal += 1
		uid = info[0]
		row = info[1]
		dataTableColumns = row.keys()
		action = '<div class="btn-group btn-group-xs">\
					<input class="uid" type="hidden" value="'+ str(uid) +'" />\
					<button type="button" name="btn_delete" data-container="body" data-toggle="tooltip" data-placement="left" title="'+_('Delete')+'" class="btn btn-default btn_delete"><i class="fa fa-trash-o"></i></button>\
					<button type="button" name="btn_edit" data-container="body" data-toggle="tooltip" data-placement="right" title="'+_('Edit')+'" class="btn btn-default btn_edit"><i class="fa fa-edit"></i></button>\
				</div>'

		for column in dataTableColumns:
			if column != 'rights' :
				res[d_search_options['columns'][column]] = row[column]
			else:
				if row['rights']:
					for right in row['rights']:
						plugin += '{0},'.format(right['plugin_name'])

					plugin = plugin[:-1]
					res['plugin'] = plugin
					plugin = ''
				else:
					res['plugin'] = ''


		res['action'] = action
		val_ret['data'].append(res.copy())
		res = {}

	val_ret['recordsTotal'] = recordsTotal
 
	return jsonp(request, val_ret)


def getPluginList(user='all'):

	d_search_options = {}
	l_plugin = []
###
# @ToDo Par defaut la fonction renvois tous les agent mais s'il sagit d'une requete
# avec un user en param alors on renvois juste les superviseurs pour ce user
###

	d_search_options['user'] = user
	d_search_options['fields'] = 'plugin_info'
	d_search_options['filter'] = 'all'

	l_plugin_res = IMDB_psg.search(collection='plugin', search_parameter=d_search_options)

	for plugin in l_plugin_res:
		l_plugin.append({'plugin_name' : plugin[0]['plugin_name'], 'short_desc' : plugin[0]['short_desc'] , 'description' : plugin[0]['description']})

	return l_plugin

@inman.post('/im_user')
@inman.get('/im_user')
def W_user():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_user.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_plugin')
@inman.get('/im_plugin')
def W_user():
	global env

	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_plugin.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_list_plugin_info')
@inman.get('/im_list_plugin_info')
def A_getListPluginInfo():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	l_result = getPluginList()

	val_ret["results"] = l_result

	return jsonp(request, val_ret)

@inman.post('/im_list_plugin')
@inman.get('/im_list_plugin')
def A_getListPlugin():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	l_result = getPluginList()
	for result in l_result:
		# Rajout dans le IF du fait que le superviseur soit dans liste de droit du user ou pas
		if re.search(request.query.get('q'), result['plugin_name'], re.IGNORECASE) is not None:
			res.append({'id': result['plugin_name'], 'text': result['plugin_name']})

	val_ret["results"] = res

	return jsonp(request, val_ret)


#################################################
### *********************************************
### OLD FASHION Master Part
### *********************************************
#################################################



def collectMonitoringconf(d_agent_info, agent_oid):

	agent_conf_oid = None

	agent_oid = getOidInDB('agent_list', d_agent_info['agent_alias'])

	d_agent_info['in_update'] = 1
	IMDB.update(collection='agent_list', doc=d_agent_info, id=agent_oid)

	agent = ClassAgent(d_agent_info, IMDB)
	try:
		agent.connect()
	except Exception, e:
		raise e

	while True:
		try:
			time.sleep(1)
			l_hostlist = agent.getListHosts()
			l_hostconfig = agent.getListHostsconfig()
			l_servicelist = agent.getListServices()
			l_servicetemplate = agent.getListServicestemplate()
			l_hosttemplate = agent.getListHoststemplate()

			insertConfInDB('HostList', d_agent_info['agent_alias'], l_hostlist)
			insertConfInDB('HostConfig', d_agent_info['agent_alias'], l_hostconfig)
			insertConfInDB('ServicesList', d_agent_info['agent_alias'], l_servicelist)
			insertConfInDB('Servicestemplate', d_agent_info['agent_alias'], l_servicetemplate)
			insertConfInDB('Hoststemplate', d_agent_info['agent_alias'], l_hosttemplate)

			agent.close()
			d_agent_info['in_update'] = 0
			IMDB.update(collection='agent_list', doc=d_agent_info, id=agent_oid)
			break
		except Exception, e:
			print e
			raise e
			##pass

@inman.post('/register_agent')
def register_agent():

	agent_oid = None
	agent_in_update = 0

	d_agent_info = request.json

	print '****************'
	print d_agent_info
	print '****************'

	if d_agent_info['agent_connection_type'] == 'SSH':
		port_ssh_tunnel = define_tunnel_port(d_agent_info)
		d_agent_info['port_ssh_tunnel'] = port_ssh_tunnel

#	pprint.pprint(IMDB.selectall(collection='HostConfig'))
#	IMDB.flush(collection='agent_list')
#	IMDB.flush(collection='agent_ref')

	agent_oid = getOidInDB('agent_list', d_agent_info['agent_alias'])

#	print 'Agent Name: '+d_agent_info['agent_alias']
#	if agent_oid is not None:
#		print 'Agent OID: '+agent_oid
#	else:
#		print 'Agent OID: None'
#	print ''

	agent_in_update = isAgentInUpdate('agent_list', d_agent_info['agent_alias'])

	if agent_oid is not None:
		if agent_in_update == 0:
			d_agent_info['in_update'] = 0
			IMDB.update(collection='agent_list', doc=d_agent_info, id=agent_oid)
	else:
		d_agent_info['in_update'] = 0
		res = IMDB.publish(collection='agent_list', doc=d_agent_info)
		IMDB.publish(collection='agent_ref', doc={'agent_alias': d_agent_info['agent_alias'], 'oid': res['_id']})

	if d_agent_info['in_update'] == 0:
		collectMonitoringconf(d_agent_info, agent_oid)

@inman.post('/getlistsupervisor')
@inman.get('/getlistsupervisor')
def getListSupervisor():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}
	oldID = None

	##Fonction qui liste les agent_alias authorise en fonction du user et donc font la liste des OR pour le AND

	t_result = getAgentList()
	for result in t_result:
		# Rajout dans le IF du fait que le superviseur soit dans liste de droit du user ou pas
		if re.search(request.query.get('q'), result['agent_alias'], re.IGNORECASE) is not None and oldID != result['agent_alias']:
			res.append({'id': result['agent_alias'], 'text': result['agent_alias']})

	val_ret["results"] = res

	return jsonp(request, val_ret)

def getConfInfo(db_collection_name, entry, type=None, agent_alias=None):

	if agent_alias == None:
		d_search_options = {\
			'query' :\
			{\
				'filtered' :\
				{ \
					'filter' : \
					{\
						'bool' :\
						{\
							'must' :\
							[\
	##							{'term' : \ ###### Parama a utiliser avec la restriction user droit sur les superviseurs
	##							{ \
	##								'agent_alias': agent_alias.lower()\
	##							}},\
								{'term' : \
								{ \
									db_collection_name: entry.lower()\
								}}\
							]\
						}\
					}\
				}\
			}\
		}
	else:
		d_search_options = {\
			'query' :\
			{\
				'filtered' :\
				{ \
					'filter' : \
					{\
						'bool' :\
						{\
							'must' :\
							[\
								{'term' : \
								{ \
									'agent_alias': agent_alias.lower()\
								}},\
								{'term' : \
								{ \
									db_collection_name: entry.lower()\
								}}\
							]\
						}\
					}\
				}\
			}\
		}

	l_results = IMDB.search(collection=db_collection_name, search_parameter=d_search_options)

	##Fonction qui liste les services pour un host authorise en fonction du user et donc font la liste des OR pour le AND

	if type != None:
		if type in l_results[0]['_source'][entry]:
			return l_results[0]['_source'][entry][type]
		else:
			return []
	else:
		return l_results[0]['_source'][entry]

@inman.post('/gethostmacros/<hostname>')
@inman.get('/gethostmacros/<hostname>')
def getHostMacros(hostname):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	##Fonction qui liste les services pour un host authorise en fonction du user et donc font la liste des OR pour le AND
	macros = getConfInfo('HostConfig' , hostname, 'macros')
	for macro in macros:  
		res.append({'name': macro['name'], 'value': macro['value']})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/gethostservices/<hostname>')
@inman.get('/gethostservices/<hostname>')
def getHostServices(hostname):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	##Fonction qui liste les services pour un host authorise en fonction du user et donc font la liste des OR pour le AND
	services = getConfInfo('HostConfig' , hostname, 'services')
	for service in services:  
		res.append({'name': service['service_description'], 'template': service['use']})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/gethostconffilepath/<hostname>')
@inman.get('/gethostconffilepath/<hostname>')
def getHostConfFilepath(hostname):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	##Fonction qui recupere le chemin du fichier de conf pour un host authorise en fonction du user et donc font la liste des OR pour le AND
	filepath = getConfInfo('HostConfig' , hostname, 'filepath')

	return filepath
#	if parents != None:
#		for parent in parents:  
#			res.append({'id': parent, 'text': parent})
#
#	val_ret["results"] = res
#
#	return jsonp(request, val_ret)

@inman.post('/gethostparents/<hostname>')
@inman.get('/gethostparents/<hostname>')
def getHostParents(hostname):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	##Fonction qui liste les services pour un host authorise en fonction du user et donc font la liste des OR pour le AND
	parents = getConfInfo('HostConfig' , hostname, 'parents')
	if parents != None:
		for parent in parents:  
			res.append({'id': parent, 'text': parent})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/gethostusetemplate/<hostname>')
@inman.get('/gethostusetemplate/<hostname>')
def getHostUsetemplate(hostname):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	##Fonction qui liste les services pour un host authorise en fonction du user et donc font la liste des OR pour le AND
	usetemplates = getConfInfo('HostConfig' , hostname, 'use')
	for usetemplate in usetemplates:  
		res.append({'id': usetemplate, 'text': usetemplate})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/gethostgroups/<hostname>')
@inman.get('/gethostgroups/<hostname>')
def getHostHostgroup(hostname):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	##Fonction qui liste les services pour un host authorise en fonction du user et donc font la liste des OR pour le AND
	groups = getConfInfo('HostConfig' , hostname, 'hostgroups')
	for group in groups:  
		res.append({'id': group, 'text': group})

	val_ret["results"] = res

	return jsonp(request, val_ret)

def getList(db_collection_name, type=None, supervisor='all', spec=False):
	ret = []

	if supervisor == 'all':
		d_search_options = {\
			'query' :\
			{\
				'filtered' :\
				{ \
					'filter' : \
					{\
						'bool' :\
						{\
							'must' :\
							[\
##								{'term' : \
##								{ \
##									'agent_alias': agent_alias.lower()\
##								}},\
							]\
						}\
					}\
				}\
			}\
		}
	else:
		d_search_options = {\
			'query' :\
			{\
				'filtered' :\
				{ \
					'filter' : \
					{\
						'bool' :\
						{\
							'must' :\
							[\
								{'term' : \
								{ \
									'agent_alias': supervisor.lower()\
								}},\
							]\
						}\
					}\
				}\
			}\
		}

	l_results = IMDB.search(collection=db_collection_name, search_parameter=d_search_options)

	##Fonction qui fabrique une liste suivant la collection et ou la collection et l'info de la collection authorise en fonction du user et donc font la liste des OR pour le AND

	if type != None:
		for result in l_results:
			if isinstance(result['_source'][result['_source'][db_collection_name]][type], list):
				for info in result['_source'][result['_source'][db_collection_name]][type]:
					ret.append(info)
			else:
				ret.append(result['_source'][result['_source'][db_collection_name]][type])
		return ret
	elif spec == True:
		for result in l_results:
			ret.append(result['_source'])
		return ret
	else:
		for result in l_results:
			ret.append(result['_source'][result['_source'][db_collection_name]])
		return ret

@inman.post('/getallhost/<supervisor>')
@inman.get('/getallhost/<supervisor>')
def getAllHost(supervisor='all'):
	response.content_type = 'application/json'
	res = []

	supervisor = request.query.get('supervisor')

	##Fonction qui liste les infos de tous les hosts authorise en fonction du user et donc font la liste des OR pour le AND

	l_hosts = getList('HostConfig', supervisor=supervisor)
	for host in l_hosts:
		res.append(host)

	return jsonp(request, res)

@inman.post('/getlisthostinfo/<supervisor>')
@inman.get('/getlisthostinfo/<supervisor>')
def getListHostinfo(supervisor='all'):
	response.content_type = 'application/json'
	val_ret = {'draw': 10, 'recordsTotal': 0, 'recordsFiltered': 10, 'data': []}
	res = {}
	recordsTotal = 0

	##Fonction qui liste les host info authorise en fonction du user et donc font la liste des OR pour le AND

	l_hosts = getList('HostConfig', supervisor=supervisor)

	for host in l_hosts:
		recordsTotal += 1
		res['superviseur'] = host['supervisor_name'] 
		res['hote'] = host['host_name']
		res['ip'] = host['address']
		if 'alias' in host:
			res['nom'] = host['alias']
		else:
			res['nom'] = None
		res['action'] = '<div class="btn-group btn-group-xs">\
							<button type="button" name="btn_delete" data-container="body" data-toggle="tooltip" data-placement="left" title="'+_('Delete host')+'" class="btn btn-default btn_delete"><i class="fa fa-trash-o"></i></button>\
							<button type="button" name="btn_edit" data-container="body" data-toggle="tooltip" data-placement="right" title="'+_('Edit host')+'" class="btn btn-default btn_edit"><i class="fa fa-edit"></i></button>\
						</div>'
		val_ret['data'].append(dict(res))
		res = {}

	val_ret['recordsTotal'] = recordsTotal
 
	return jsonp(request, val_ret)

@inman.post('/getlisthost/<supervisor>')
@inman.get('/getlisthost/<supervisor>')
def getListHost(supervisor='all'):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	###
	# Le besoin de recup superviseur est du au fait qu'il ne faut pas tout récup si un seul superviseur est déjà choisi
	###

	##Fonction qui liste les agent_alias authorise en fonction du user et donc font la liste des OR pour le AND

	l_hosts = getList('HostConfig', supervisor=supervisor)

	for host in l_hosts:
		if re.search(request.query.get('q'), host['host_name'], re.IGNORECASE) is not None:
			if host['supervisor_name'] not in ret:
				ret[host['supervisor_name']] = [{'id': host['supervisor_name']+ ':' +host['host_name'], 'text': host['host_name']}]
			else:
				ret[host['supervisor_name']].append({'id': host['supervisor_name']+ ':' +host['host_name'], 'text': host['host_name']})

	for supervisor, hostlist in ret.items():
		res.append({'text': supervisor, 'children': hostlist})

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/getlistgroup')
@inman.get('/getlistgroup')
def getListHostgroup():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	list_group = []
	res = []
	ret = {}

	l_groups = getList('HostConfig', 'hostgroups')
	
	##Fonction qui liste les group authorise en fonction du user et donc font la liste des OR pour le AND

	for group in l_groups:
		if group not in list_group:
			if re.search(request.query.get('q'), group, re.IGNORECASE) is not None:
				list_group.append(group)
				res.append({'id': group, 'text': group})
					
	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/getlistusetemplate')
@inman.get('/getlistusetemplate')
def getListUsetemplate():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	list_usetemplate = []
	res = []
	ret = {}

	l_usetemplates = getList('HostConfig', 'use')
	##Fonction qui liste les group authorise en fonction du user et donc font la liste des OR pour le AND

	for usetemplate in l_usetemplates:
		if usetemplate not in list_usetemplate:
			if re.search(request.query.get('q'), usetemplate, re.IGNORECASE) is not None:
				list_usetemplate.append(usetemplate)
				res.append({'id': usetemplate, 'text': usetemplate})
					
	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/getlistservices/<supervisor>')
@inman.get('/getlistservices/<supervisor>')
def getListServices(supervisor='all'):
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	##Fonction qui liste les services authorise en fonction du user et donc font la liste des OR pour le AND

	l_services = getList('ServicesList', supervisor=supervisor)

	for service in l_services:
		if re.search(request.query.get('q'), service['use'], re.IGNORECASE) is not None:
			res.append({'id': service['service_description']+' #'+service['use'], 'text': service['service_description']+' #'+service['use']})
					
	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/getcollection/<db_collection>/<supervisor>')
@inman.get('/getcollection/<db_collection>/<supervisor>')
def getCollection(db_collection, supervisor='all'):
	response.content_type = 'application/json'
	ret = {}

	d_db_collection = getList(db_collection, supervisor=supervisor, spec=True)

#	pprint.pprint(d_db_collection)

	for entry in d_db_collection:
		ret[entry[db_collection]] = entry

	return json.dumps(ret)

def isHostnameInUse(hostname, supervisor, oid):

	oid_in_db = getOidInDB('HostConfig', supervisor, hostname)

	if oid != oid_in_db and oid_in_db != None:
		return True

	return False

def insertInDB(db_collection_name, agent_alias, idKey, confInfo, oid = None):

	confEntry = {'db_collection': db_collection_name, 'agent_alias': agent_alias, db_collection_name: idKey, idKey: confInfo}

	pprint.pprint(confEntry)

	if oid is not None:
		IMDB.update(collection=db_collection_name, doc=confEntry, id=oid)
	else:
		res = IMDB.publish(collection=db_collection_name, doc=confEntry)
		IMDB.publish(collection=db_collection_name+'_ref', doc={'agent_alias': agent_alias, db_collection_name: idKey, 'oid': res['_id']})

@inman.post('/deletehostindb')
@inman.get('/deletehostindb')
def deleteHostInDB():
	oid = None

	hostTodelete = request.query.get('hosttodelete')
	supervisor = request.query.get('supervisor')

	oid = getOidInDB('HostList', supervisor, hostTodelete)
	IMDB.delete('HostList', oid)
##	IMDB.delete('HostList_ref', oid)

	oid = getOidInDB('HostConfig', supervisor, hostTodelete)
	IMDB.delete('HostConfig', oid)
##	IMDB.delete('HostConfig_ref', oid)

'''
	with ejdb.find('agent_conf_ref', {'db_collection': 'HostList', '$and': [{'agent_alias': supervisor}, {'HostList': hostTodelete}]}) as agent_conf_ref_list:
		for agent_conf_ref in agent_conf_ref_list:
			agent_conf_oid = agent_conf_ref['oid']

	ejdb.remove('agent_conf', agent_conf_oid)
	ejdb.remove('agent_conf_ref', agent_conf_ref['_id'])

	agent_conf_ref = None
	agent_conf_oid = None

	with ejdb.find('agent_conf_ref', {'db_collection': 'HostConfig', '$and': [{'agent_alias': supervisor}, {'HostConfig': hostTodelete}]}) as agent_conf_ref_list:
		for agent_conf_ref in agent_conf_ref_list:
			agent_conf_oid = agent_conf_ref['oid']
	
	ejdb.remove('agent_conf', agent_conf_oid)
	ejdb.remove('agent_conf_ref', agent_conf_ref['_id'])
'''

@inman.post('/publishhostindb')
@inman.get('/publishhostindb')
def publishHostInDB():
	##Fonction qui fait insert ou update d'un host en DB
	services = []
	hostinfo = None
	flag_syntax = False

	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	addtype = request.query.get('addtype')
	if addtype == 'newhost':
		oid = None
	elif addtype == 'edit':
		oid = request.query.get('oid')
##		hostinfo = getConfInfo('HostConfig', request.query.get('hostname'))
	else:
		## addtype == 'template'
##		hostinfo = getConfInfo('HostConfig', request.query.get('hostname'))
		oid = None

#	hostinfo = json.loads(hostinfo[ hostinfo.index("(") + 1 : hostinfo.rindex(")") ])['results']
#	if hostinfo:
#		hostinfo = hostinfo[0]

#	print '---****---'
#	print pprint.pprint(hostinfo)
#	print '---****---'

	conf_filepath = request.query.get('conf_filepath')
	use = request.query.get('use_template').split(',')
	hostname = request.query.get('hostname')
	hostgroups = request.query.get('group').split(',')
	alias = request.query.get('alias')
	address = request.query.get('ip')
	supervisor = request.query.get('supervisor')
	parents = request.query.get('parents').split(',')

	if isHostnameInUse(hostname, supervisor, oid):
		res.append(_('Hostname already in use')+'. '+_('Not allowed to have the same hostname more than once'))
		response.status = '412 '+_('Hostname already in use')
		flag_syntax = True

	if re.search('[`~!$%^&*\"|\'<>?,()=]', hostname):
		res.append(_('Syntax construction problem for ')+_('Hostname')+_(' in ')+hostname+'. '+_('Not supported character : ')+'`~!$%^&*\"|\'<>?,()=')
		response.status = '412 '+_('Syntax conflict')
		flag_syntax = True
	if not re.match('^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address):
		res.append(_('Syntax construction problem for ')+_('IP')+_(' in ')+address)
		response.status = '412 '+_('Syntax conflict')
		flag_syntax = True
	if re.search('[`~!$%^&*\"|\'<>?,()=]', alias):
		res.append(_('Syntax construction problem for ')+_('Alias')+_(' in ')+alias+'. '+_('Not supported character : ')+'`~!$%^&*\"|\'<>?,()=')
		response.status = '412 '+_('Syntax conflict')
		flag_syntax = True

	i = 0
	for parent in parents:
		if parent != '' and ':' in parent:
			parent = parent[parent.index(':')+1:]
			parents[i] = parent
		elif parent != '':
			parents[i] = parent
		else:
			parents = None
		i += 1

	macros = json.loads(request.query.get('macros'))

	for macro in macros:
		if re.search('[`~$^&\"|\'<>]', macro['value']):
			res.append(_('Syntax construction problem for ')+_('Macro value')+_(' in ')+macro['value']+'. '+_('Not supported character : ')+'`~!$%^&*\"|\'<>?,()=')
			response.status= '412 '+_('Syntax conflict')
			flag_syntax = True
		if re.search('[`~!$%^&*\"|\'<>?,()=]', macro['name']):
			res.append(_('Syntax construction problem for ')+_('Macro name')+_(' in ')+macro['name']+'. '+_('Not supported character : ')+'`~!$%^&*\"|\'<>?,()=')
			response.status = '412 '+_('Syntax conflict')
			flag_syntax = True

	l_services = json.loads(request.query.get('services'))

	for service in l_services:
		if service:
			serviceinfo = getConfInfo('ServicesList', service, agent_alias=supervisor)
			serviceinfo['host_name'] = hostname
			services.append(serviceinfo.copy())

	############
	## @TODO 
	## Il faut penser a reprendre tous les champs en cas de edit ou template comme le champ note
	## meme si pas dispo dans le formulaire de la page
	############

	confInfo = {'filepath': conf_filepath,\
				'use': use,\
				'host_name': hostname,\
				'hostgroups': hostgroups,\
				'alias': alias,\
				'address': address,\
				'supervisor_name': supervisor,\
				'parents': parents,\
				'macros': macros,\
				'services': services\
	}

	if not flag_syntax:
		## Try Catch pour recup des pb d'insert et push dans le catch sur le res
		insertInDB('HostConfig', supervisor, hostname, confInfo, oid)
#####
## Il y a une erreur d'insertion en base avec les lignes ci-dessous
#		oid = getOidInDB('HostList', supervisor, hostname)
#		insertInDB('HostList', supervisor, hostname, {'HostList': hostname, hostname: hostname, 'agent_alias': supervisor}, oid)
#		pass
#####

	val_ret["results"] = res

	return jsonp(request, val_ret)

@inman.post('/im_crudhost/<type>')
@inman.get('/im_crudhost/<type>')
def createHost(type):
	global env

	d_hostservices = {"more": False, "results":[]}
	d_hostmacros = {"more": False, "results":[]}
	d_hostgroups = []
	d_usetemplate = []
	d_parents = []
	conf_filepath = ''

	hostname = request.forms.get('hostname_'+type)
	alias = request.forms.get('alias_'+type)
	ip = request.forms.get('ip_'+type)
	template_name = request.forms.get('templatemodel')
	supervisor = request.forms.get('supervisor_newhost')

	if template_name:
		t_template = template_name.split(':')
		template_name = t_template[1]
		supervisor = t_template[0]
		if type == 'template':
			host = hostname
		else:
			host = template_name
	else:
		host = hostname

	if type == 'edit':
		oid = getOidInDB('HostConfig', supervisor, host)
	else:
		oid = None

	if template_name != None:
		d_hostservices = getHostServices(template_name)
		d_hostservices = json.loads(d_hostservices)

		d_hostmacros = getHostMacros(template_name)
		d_hostmacros = json.loads(d_hostmacros)

		d_hostgroups = getHostHostgroup(template_name)
		d_hostgroups = json.loads(d_hostgroups)
		d_hostgroups = str(json.dumps(d_hostgroups['results']))

		d_usetemplate = getHostUsetemplate(template_name)
		d_usetemplate = json.loads(d_usetemplate)
		d_usetemplate = str(json.dumps(d_usetemplate['results']))

		d_parents = getHostParents(template_name)
		d_parents = json.loads(d_parents)
		d_parents = str(json.dumps(d_parents['results']))

		conf_filepath = getHostConfFilepath(template_name)

	d_supervisor = str(json.dumps({'id': supervisor, 'text': supervisor}))

	d_render = {'page_title': 'InMan - Configuration management tool', 'page_header_name': host, 'addtype': type, 'oid': oid, 'hostname': host, 'ip': ip, 'alias': alias, 'group_list': d_hostgroups, 'use_template_list': d_usetemplate, 'services': d_hostservices['results'], 'macros': d_hostmacros['results'], 'supervisor_name_arg': d_supervisor, 'parents_list': d_parents, 'conf_filepath': conf_filepath}

	response.content_type = 'text/html'
	OTemplate = env.get_template('im_host.tpl')

	return OTemplate.render(d_render)

@inman.post('/getprogresssync')
@inman.get('/getprogresssync')
def getProgressSync():

	response.content_type = 'application/json'

	supervisor = request.query.get('supervisor')
	ret = []
	
	if isfile("./progress_"+supervisor):
		fd = file("./progress_"+supervisor, 'rw+')
		for line in fd:
			ret.append(line)
		fd.truncate(0)
		fd.close()

	return jsonp(request, ret)

@inman.post('/pushprogresssync')
@inman.get('/pushprogresssync')
def pushProgressSync():

	response.content_type = 'application/json'

	d_progress_info = request.json
	
	print d_progress_info
	fd = file("./progress_"+d_progress_info['agent_alias'], 'a')
	fd.write(json.dumps(d_progress_info)+"\n")
	fd.close()

	return jsonp(request, d_progress_info)

@inman.post('/launchsync')
@inman.get('/launchsync')
def launchSyncSupervisor():

	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[]}
	res = []
	ret = {}

	collection2Sync = request.query.get('collection2Sync')
	supervisor = request.query.get('supervisor')
	l_agent = getAgentList(supervisor=supervisor)
	d_agent_info = l_agent[0]

	try:
		response.status = '202 '+_('Synchronization in progress')
		agent = ClassAgent(d_agent_info, IMDB)
		agent.connect()
		agent.initSyncSupervisor(collection2Sync)
		agent.close
#		res.append(_('Synchronization complete'))
		val_ret["results"] = res
		return jsonp(request, val_ret)
	except Exception, e:
		print e
		response.status = '444 '+_('Connection Failed')
		res.append(_('Synchronization failure')+' - '+_('Connection Failed'))
		val_ret["results"] = res
		print e
		return jsonp(request, val_ret)

@inman.post('/syncconf')
@inman.get('/syncconf')
def syncConf():

	response.content_type = 'application/json'

	d_sync_info = request.json

	supervisor = d_sync_info['agent_alias']
	db_collection = d_sync_info['collection2Sync']

	dataCollection = getCollection(db_collection, supervisor)

	return jsonp(request, dataCollection)

def getUserSessionPluginList():

	l_plugin = []

	s = inman.request.environ.get('beaker.session')

	for right in s['rights']['rights']:
		l_plugin.append(right['plugin_name'])

	return l_plugin

@inman.post('/')
@inman.get('/')
def main():

	logger.info('Access page -> Name : {0}, URI : {1}'.format('main', '/'))
	
	verif_session()

	plugin_list = getUserSessionPluginList()

	d_render = {'page_title': 'InMan - Configuration management tool', 'plugin_list': plugin_list}

	OTemplate = env.get_template('im_dashboard.tpl')

	return OTemplate.render(d_render)

@inman.post('/im_masteralive')
@inman.get('/im_masteralive')
def master_alive():

	return 'ok'

def getUserSessionRight(login):
	d_search_options = {}

	d_search_options['filter'] = 'user_info->>\'login\' = \''+ login.lower() +'\''
	d_search_options['fields'] = 'id, json_build_object(\'rights\', user_info->\'rights\')'

	l_user_res = IMDB_psg.search(collection='users', search_parameter=d_search_options)

	rights = l_user_res[0][1]

	return rights

@inman.post('/im_login')
@inman.get('/im_login')
def im_login():

	login_failed = None

	if request.forms.get('login'):
		login = request.forms.get('login')
		password = request.forms.get('password')

		if isInmanUser(login, password=password):
			s = inman.request.environ.get('beaker.session')
			s['login'] = login
			s['rights'] = getUserSessionRight(login)
			redirect('/')
		else:
			login_failed = True

	d_render = {'page_title': 'InMan - Configuration management tool', 'login_failed' : login_failed}
	OTemplate = env.get_template('im_login.tpl')
	return OTemplate.render(d_render)

@inman.post('/cas_logout')
@inman.get('/cas_logout')
def cas_logout():

	try:
		logger.info('SSO Session stop'.format())
		
		session = inman.request.environ.get('beaker.session')
		logger.debug('SSO Session info : {0}'.format(session))

		status, userid, cookie = pycas.pycas.logout(CAS_SERVER, SERVICE_URL, web_session=session, secure=False)
		logger.debug('SSO logout -> status : {0}, userid : {1}, cookie : {2}'.format(status, userid, cookie))

		if status == 1:
			logger.debug('SSO Logout Redirect to : {0}'.format(userid))
			redirect(userid)

		logger.debug('SSO Logout NO redirection'.format())

	except Exception, e:
		logger.error('SSO Session logout Failed : {0}'.format(e))
		raise e
	

@inman.post('/cas_login')
@inman.get('/cas_login')
def cas_login():

	try:
		logger.info('SSO Session start'.format())
		session = inman.request.environ.get('beaker.session')
		logger.debug('SSO Session info : {0}'.format(session))

		status, userid, cookie = pycas.pycas.login(CAS_SERVER, SERVICE_URL, web_session=session, secure=False)
		logger.debug('SSO login -> status : {0}, userid : {1}, cookie : {2}'.format(status, userid, cookie))

		if status == 1:
			logger.debug('SSO Login Redirect to : {0}'.format(userid))
			redirect(userid)
		else:
			session['rights'] = getUserSessionRight(session['login'])
			logger.debug('SSO Get user right : {0}'.format(session['rights']))
			logger.debug('SSO Login Redirect to : {0}'.format('/'))
			redirect('/')

	except Exception, e:
		logger.error('SSO Session login Failed : {0}'.format(e))
		raise e

@inman.route('/test')
def test():

	print request.GET.allitems()
	print request.POST.allitems()

	s = inman.request.environ.get('beaker.session')
	s['test'] = s.get('test',0) + 1
	s.save()

	return 'Test counter: %d' % s['test']

try:
	logger.info('Start InMan server. Listening on http://{0}:{1}/'.format('0.0.0.0', 80))
	inman.run(app=app, host='0.0.0.0', port=80, server='cherrypy')	
except Exception, e:
	logger.error('Failed to start InMan server : {0}'.format(e))
	ch.close()
	raise e