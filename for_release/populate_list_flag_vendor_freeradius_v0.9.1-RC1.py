#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# For v0.9.1-RC1
####

#~~~~~~~~~~~~~~~~~
# To move from previous version to v0.9.1-RC1
# MATVIEW Add RADIUS name into Vendor FLAG List for Freeradius plugin
# Matview name : list_flag_vendor_freeradius
# Old format : [{"vendorname": "HP-Procurve", "l_flag": [{"Service-Type": ""}, {"HP-Command-Exception": ""}, {"Hp-Command-String": ""}]}]
# New format : [{"vendorname": "HP-Procurve", "radiusname": "Radius IRIS Recette", "l_flag": [{"Service-Type": ""}, {"HP-Command-Exception": ""}, {"Hp-Command-String": ""}]}]
#~~~~~~~~~~~~~~~~~

import json
import psycopg2

# UPDATE matview SET (view_data) = ('[{"l_flag": [{"Xylan-Asa-Access": ""}, {"Xylan-Acce-Priv-F-R1": ""}, {"Xylan-Acce-Priv-F-R2": ""}, {"Xylan-Acce-Priv-F-W1": ""}, {"Xylan-Acce-Priv-F-W2": ""}], "radiusname": "Radius IRIS Recette", "vendorname": "ALU-Omniswitch"}, {"l_flag": [{"Service-Type": ""}, {"cisco-avpair": ""}], "radiusname": "Radius IRIS Recette", "vendorname": "C-Cisco"}, {"l_flag": [{"Service-Type": ""}, {"HP-Command-Exception": ""}, {"Hp-Command-String": ""}], "radiusname": "Radius IRIS Recette", "vendorname": "HP-Procurve"}]') WHERE id = '2'

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
d_search_options['filter'] = 'name = \'list_flag_vendor_freeradius\''

l_results = IMDB.search(collection='matview', search_parameter=d_search_options)

d_search_options['fields'] = 'json_build_object(\'radiusname\', vendor_info->>\'radiusname\', \'vendorname\', vendor_info->>\'vendorname\', \'l_block_flag\', vendor_info->>\'l_flag_level\')'
d_search_options['filter'] = 'all'
l_vendor_with_flag = IMDB.search(collection='vendor_freeradius', search_parameter=d_search_options)

for vendor_with_flag in l_vendor_with_flag :

	l_flag = []
	l_block = json.loads(vendor_with_flag[0]['l_block_flag'])
	l_block = l_block[0]['l_block']

	for block_info in l_block:
		for flag in block_info['list']:
			l_flag.append(flag)

	l_to_view.append({'radiusname': vendor_with_flag[0]['radiusname'], 'vendorname': vendor_with_flag[0]['vendorname'], 'l_flag': l_flag})

to_insert = json.dumps(l_to_view).replace('\'', '\'\'')

doc['view_data'] = to_insert

if l_results :

	uid = l_results[0][0]
	d_search_options['fields'] = ''
	d_search_options['filter'] = 'id = \''+ str(uid) +'\''

	IMDB.update('matview', doc, id=uid, search_parameter=d_search_options)

else:
	IMDB.publish('matview', doc)

