#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# For v0.9-RC2
####

#~~~~~~~~~~~~~~~~~
# To move from previous version to v0.9-RC1
# Need for list of client in Network Perimeter IP List part of Freeradius plugin
#~~~~~~~~~~~~~~~~~

import json
import psycopg2

# UPDATE matview SET (view_data) = ('["192.168.42.42", "172.85.20.2"]') WHERE name = 'list_client_freeradius'

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

d_search_options['fields'] = 'view_data'
d_search_options['filter'] = 'name = \'list_client_freeradius\''

l_results = IMDB.search(collection='matview', search_parameter=d_search_options)

d_search_options['fields'] = 'client_info->>\'ip\' AS IP'
d_search_options['filter'] = 'all'
l_ip = IMDB.search(collection='client_freeradius', search_parameter=d_search_options)
	
for ip in l_ip :
	l_ip_to_view.append(ip[0])

to_insert = json.dumps(l_ip_to_view).replace('\'', '\'\'')

doc['name'] = 'list_client_freeradius'
doc['view_data'] = to_insert

if l_results :

	d_search_options['fields'] = ''
	d_search_options['filter'] = 'name = \'list_client_freeradius\''

	IMDB.update('matview', doc, search_parameter=d_search_options)

else :

	IMDB.publish('matview', doc)
