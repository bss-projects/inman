#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# For v0.9.1-RC1
####

#~~~~~~~~~~~~~~~~~
# To move from previous version to v0.9.1-RC1
# MATVIEW Add RADIUS name into Right List for Freeradius plugin
# Matview name : list_right_freeradius
# Old format : ["rwAll_admin"]
# New format : [{"radiusname": "Radius IRIS Recette", "right": "rwAll_admin"}]
#~~~~~~~~~~~~~~~~~

import json
import psycopg2

# UPDATE matview SET (view_data) = ('[{"right": "rwAll_admin", "radiusname": "Radius IRIS Recette"}]') WHERE id = '3'

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
l_to_view = []
to_insert = ''
IMDB = DBManagement()

d_search_options['fields'] = 'id, view_data'
d_search_options['filter'] = 'name = \'list_right_freeradius\''

l_results = IMDB.search(collection='matview', search_parameter=d_search_options)

d_search_options['fields'] = 'json_build_object(\'radiusname\', vendor_info->>\'radiusname\', \'vendorname\', vendor_info->>\'vendorname\', \'l_flag_level\', vendor_info->>\'l_flag_level\')'
d_search_options['filter'] = 'all'
l_vendor_with_right = IMDB.search(collection='vendor_freeradius', search_parameter=d_search_options)

for vendor_with_right in l_vendor_with_right :
	radiusname = vendor_with_right[0]['radiusname']
	l_flag_level = json.loads(vendor_with_right[0]['l_flag_level'])

	right = {}
	for flag_level in l_flag_level:
		if flag_level['label'] != 'list_flag':
			right = {'radiusname': radiusname, 'right': flag_level['label']}
			if {'radiusname': radiusname, 'right': flag_level['label']} not in l_to_view:
				l_to_view.append(right)

to_insert = json.dumps(l_to_view).replace('\'', '\'\'')

doc['view_data'] = to_insert

if l_results :

	uid = l_results[0][0]
	d_search_options['fields'] = ''
	d_search_options['filter'] = 'id = \''+ str(uid) +'\''

	IMDB.update('matview', doc, id=uid, search_parameter=d_search_options)

else:
	IMDB.publish('matview', doc)

