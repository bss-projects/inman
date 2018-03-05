#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# For v0.9.3-RC1
####

#~~~~~~~~~~~~~~~~~
# To move from previous version to v0.9.3-RC1
# User need to have an expiration date for each account.
# This script init every expiration date in a year for each user who don't have any
#~~~~~~~~~~~~~~~~~

import datetime
import json
import psycopg2
import time

# UPDATE users_freeradius SET (user_info) = ('{"username": "ab704961", "right": "rwAll_admin", "expiration_date": "21/07/2018", "isldap": "true", "radiusname": "Radius IRIS", "expiration_status": "ok", "password": ""}') WHERE id = 48

class DBManagement(object):
	"""docstring for DBManagement"""
	def __init__(self,  host='localhost', database='inman', user='dbu_inman', password='pass', port=5432):
		super(DBManagement, self).__init__()
		self.database = database
		self.search_res = None
		self.get_res = None
		self.conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
		self.cur = ''
	
	def execute_query(self, query):
		self.cur = self.conn.cursor()

		res = self.cur.execute(query)

		self.conn.commit()
		self.cur.close()

		return res

	def update(self, collection, doc, id=None, search_parameter=None):
		if search_parameter['filter'] == 'all':
			search_parameter['filter'] = '1=1'

		columns = ''
		vals = ''

		i = 0
		for column in doc.keys():
			if i != 0:
				columns += ', '
			columns += str(column)
			i += 1

		i = 0
		for val in doc.values():
			if i != 0:
				vals += ', '
			vals += '\''+ str(val) +'\''
			i += 1

		self.cur = self.conn.cursor()

		print "UPDATE "+ collection +" SET ("+ columns +") = ("+ vals +") WHERE "+ search_parameter['filter'] +""
		res = self.cur.execute("UPDATE "+ collection +" SET ("+ columns +") = ("+ vals +") WHERE "+ search_parameter['filter'] +"")
		self.conn.commit()

		self.cur.close()

		return res

	def publish(self, collection, doc):

		columns = ''
		vals = ''

		i = 0
		for column in doc.keys():
			if i != 0:
				columns += ', '
			columns += str(column)
			i += 1

		i = 0
		for val in doc.values():
			if i != 0:
				vals += ', '
			vals += '\''+ str(val) +'\''
			i += 1

		self.cur = self.conn.cursor()

		print "INSERT INTO "+ collection +" ("+ columns +") VALUES ("+ vals +")"
		res = self.cur.execute("INSERT INTO "+ collection +" ("+ columns +") VALUES ("+ vals +")")
		self.conn.commit()

		self.cur.close()

		return res

	def search(self, collection, search_parameter):
		
		if search_parameter['filter'] == 'all':
			search_parameter['filter'] = '1=1'

		self.cur = self.conn.cursor()

		self.cur.execute("SELECT "+ search_parameter['fields'] +" FROM "+ collection +" WHERE "+ search_parameter['filter'] +"")
		search_res = self.cur.fetchall()

		self.conn.commit()

		self.cur.close()

		return search_res

doc = {}
d_search_options = {}
l_ip_to_view = []
to_insert = ''
IMDB = DBManagement()

d_search_options['fields'] = 'id, user_info'
d_search_options['filter'] = '(user_info->\'expiration_timestamp\') IS NULL'

l_results = IMDB.search(collection='users_freeradius', search_parameter=d_search_options)

current_timestamp = time.time()
next_year_expiration_timestamp = current_timestamp + 31540000

dt = datetime.datetime.fromtimestamp(next_year_expiration_timestamp)

next_year_expiration_date = dt.strftime('%d/%m/%Y')

if l_results :
	for result in l_results:
		user_id = result[0]
		user_info = result[1]
		user_info['expiration_date'] = next_year_expiration_date
		user_info['expiration_timestamp'] = next_year_expiration_timestamp
		user_info['expiration_status'] = 'ok'

		to_insert = json.dumps(user_info).replace('\'', '\'\'')

		doc['user_info'] = to_insert

		d_search_options['fields'] = ''
		d_search_options['filter'] = 'id = {0}'.format(user_id)

		IMDB.update('users_freeradius', doc, search_parameter=d_search_options)
