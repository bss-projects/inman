#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import signal
import sys
import time
import traceback

class ClassUserTraceAction(object):
	"""docstring for ClassUserTraceAction"""
	def __init__(self, db_obj, logger):
		super(ClassUserTraceAction, self).__init__()
		self.db_obj = db_obj
		self.logger = logger
		
	def insert_action(self, user, plugin, action, action_data, agent=None):
		doc = {}
		ret = None
		to_insert = {}

		try:
			to_insert['login'] = user
			to_insert['plugin'] = plugin
			to_insert['action'] = action
			to_insert['action_data'] = action_data
			to_insert['date'] = time.time()

			if agent:
				to_insert['agent'] = agent

			to_insert = json.dumps(to_insert).replace('\'', '\'\'')

			doc['user_trace_action_info'] = to_insert

			ret = self.db_obj.publish(collection='user_trace_action', doc=doc)
		except Exception, e:
			if ret:
				self.logger.error('-- ClassUserTraceAction --\n Issue into insert_action : {0}\n Return of insert func : {1}\n Data try to be inserted : {2}\n Error stack : {3}\n'.format(e, ret, doc, traceback.format_exc()))
			else:
				self.logger.error('-- ClassUserTraceAction --\n Issue into insert_action : {0}\n No return from insert func\n Data try to be inserted : {1}\n Error stack : {2}\n'.format(e, doc, traceback.format_exc()))

	def get_action(self, uid):
		l_results = None
		d_search_options = {}

		try:
			d_search_options['fields'] = 'user_trace_action_info'
			d_search_options['filter'] = 'id = \''+ str(uid) +'\''

			l_results = self.db_obj.search(collection='user_trace_action', search_parameter=d_search_options)
		except Exception, e:
			if l_results:
				self.logger.error('-- ClassUserTraceAction --\n Issue into get_action : {0}\n Return of get func : {1}\n Search param : {2}\n Error stack : {3}\n'.format(e, l_results, d_search_options, traceback.format_exc()))
			else:
				self.logger.error('-- ClassUserTraceAction --\n Issue into get_action : {0}\n No return from get func\n Search param : {1}\n Error stack : {2}\n'.format(e, d_search_options, traceback.format_exc()))
		finally:
			return l_results

	def get_action_list(self, d_search_options):
		l_results = None

		try:
			d_search_options['fields'] = 'id, user_trace_action_info'
			#d_search_options['fields'] = 'id, json_build_object(\'plugin\', user_trace_action_info->\'plugin\', \'agent\', user_trace_action_info->\'agent\', \'action\', user_trace_action_info->\'action\', \'action_data\', user_trace_action_info->\'action_data\', \'date\', user_trace_action_info->\'date\', \'login\', user_trace_action_info->\'login\')'

			l_results = self.db_obj.search(collection='user_trace_action', search_parameter=d_search_options)
		except Exception, e:
			if l_results:
				self.logger.error('-- ClassUserTraceAction --\n Issue into get_action_list : {0}\n Return of get func : {1}\n Search param : {2}\n Error stack : {3}\n'.format(e, l_results, d_search_options, traceback.format_exc()))
			else:
				self.logger.error('-- ClassUserTraceAction --\n Issue into get_action_list : {0}\n No return from get func\n Search param : {1}\n Error stack : {2}\n'.format(e, d_search_options, traceback.format_exc()))
		finally:
			return l_results


	def get_user_action_list(self, login):
		d_search_options = {}

		d_search_options['filter'] = 'id = \''+ str(uid) +'\''
		return self.get_action_list(self, d_search_options)
		

	def get_plugin_action_list(self, plugin):
		d_search_options = {}

		d_search_options['filter'] = 'id = \''+ plugin +'\''
		return self.get_action_list(d_search_options)

	def get_agent_action_list(self, agent):
		d_search_options = {}

		d_search_options['filter'] = 'id = \''+ agent +'\''
		return self.get_action_list(d_search_options)

	def get_action_list_4_date(self, first_date, last_date=None):
		d_search_options = {}

		d_search_options['filter'] = 'id = \''+ str(uid) +'\''
		return self.get_action_list(d_search_options)

#session = inman.request.environ.get('beaker.session')
#logger.error('In function : {0}\n {1}'.format('A_deleteEntryInDB_freeradius', e))
#trace_action.insert_action(session['login'], 'Freeradius', '*FAILED* Delete in {0}'.format(collection), vendorTodelete, , agent=radiusname)