#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import psycopg2
import sys

from datetime import datetime
from elasticsearch import Elasticsearch, client

class DBManagement(object):
	"""docstring for DBManagement"""

	def __init__(self, hosts=None, database=None):
		super(DBManagement, self).__init__()
		self.es = Elasticsearch(hosts=hosts)
		self.es_client = client.IndicesClient(self.es)
		self.database = database
		self.search_res = None
		self.get_res = None

	def publish(self, collection, doc, id=None, database=None):
		if database == None:
			database = self.database

		res = self.es.index(index=database, doc_type=collection, body=doc, id=id)
		self.es_client.refresh(index=database, force=True)
		return res

	def update(self, collection, doc, id, database=None):
		if database == None:
			database = self.database

		res = self.es.index(index=database, doc_type=collection, body=doc, id=id)
		self.es_client.refresh(index=database, force=True)
		return res

	def bulkpublish(self, collection, doc, id=None, database=None):
		if database == None:
			database = self.database

		res = self.es.bulk(index=database, doc_type=collection, body=doc, id=id)
		self.es_client.refresh(index=database, force=True)
		return res

	def delete(self, collection, id, database=None):
		if database == None:
			database = self.database

		res = self.es.delete(index=database, doc_type=collection, id=id)
		self.es_client.refresh(index=database, force=True)
		return res

	def search(self, collection, search_parameter, database=None):
		i_from = 10
		if database == None:
			database = self.database

		search_res = self.es.search(index=database, doc_type=collection, body=search_parameter)
		
#		print search_res

		search_res = search_res['hits']['hits']
		res_len = len(search_res)
		self.es_client.refresh(index=database, force=True)

		if res_len == 10:
			while not res_len < 10:
				search_parameter['from'] = i_from
				i_from += 10
				res = self.es.search(index=database, doc_type=collection, body=search_parameter)
				res_len = len(res['hits']['hits'])
				search_res += res['hits']['hits']

		return search_res

	def get(self, collection, id, database=None):
		if database == None:
			database = self.database

		self.search_get = self.es.get(index=database, doc_type=collection, id=id)
		self.es_client.refresh(index=database, force=True)
		return self.search_get

	def flush(self, collection, database=None):
		if database == None:
			database = self.database

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

		l_res = self.search(collection=collection, search_parameter=d_search_options)	

		for res in l_res:
			self.delete(collection, res['_id'])

		self.es_client.refresh(index=database, force=True)

	def selectall(self, collection, database=None):
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

		i_from = 10
		if database == None:
			database = self.database

		search_res = self.es.search(index=database, doc_type=collection, body=d_search_options)
		search_res = search_res['hits']['hits']
		res_len = len(search_res)
		self.es_client.refresh(index=database, force=True)

		if res_len == 10:
			while not res_len < 10:
				d_search_options['from'] = i_from
				i_from += 10
				res = self.es.search(index=database, doc_type=collection, body=d_search_options)
				res_len = len(res['hits']['hits'])
				search_res += res['hits']['hits']

		return search_res

	def getDictResults(self):
		pass

class DBManagement_postgres(object):
	"""docstring for DBManagement_postgres"""
	def __init__(self,  host='localhost', database='inman', user='dbu_inman', password='pass', port=5432):
		super(DBManagement_postgres, self).__init__()
		self.database = database
		self.search_res = None
		self.get_res = None
		self.host = host
		self.database = database
		self.user = user
		self.password = password
		self.port = port
		self.conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
		
	def search(self, collection, search_parameter):
		
		if search_parameter['filter'] == 'all':
			search_parameter['filter'] = '1=1'

		try:
			cur = self.conn.cursor()

			cur.execute("SELECT "+ search_parameter['fields'] +" FROM "+ collection +" WHERE "+ search_parameter['filter'] +"")
		
			search_res = cur.fetchall()
		except psycopg2.Error:
			print "SELECT "+ search_parameter['fields'] +" FROM "+ collection +" WHERE "+ search_parameter['filter'] +""
			self.conn.commit()
			cur.close()
			return list()

		self.conn.commit()

		cur.close()

		return search_res

	def multi_publish(self, collection, doc):

		columns = ''
		vals = ''
		lenght = 0

		i = 0
		for column in doc.keys():
			if i != 0:
				columns += ', '
			columns += str(column)
			i += 1

		lenght = len(doc.values()[0])
		for val in doc.values()[0]:
			vals += '(\'{0}\')'.format(str(val))
			lenght -= 1
			if lenght:
				vals += ','

		cur = self.conn.cursor()

		res = cur.execute("INSERT INTO {0} ({1}) VALUES {2}".format(collection, columns, vals))
		self.conn.commit()

		cur.close()

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

		cur = self.conn.cursor()

		res = cur.execute("INSERT INTO "+ collection +" ("+ columns +") VALUES ("+ vals +")")
		self.conn.commit()

		cur.close()

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

		cur = self.conn.cursor()

		res = cur.execute("UPDATE "+ collection +" SET ("+ columns +") = ("+ vals +") WHERE "+ search_parameter['filter'] +"")
		self.conn.commit()

		cur.close()

		return res

	def delete(self, collection, id, search_parameter):
		if search_parameter['filter'] == 'all':
			search_parameter['filter'] = '1=1'

		cur = self.conn.cursor()

		res = cur.execute("DELETE FROM "+ collection +" WHERE "+ search_parameter['filter'] +"")
		self.conn.commit()

		cur.close()

		return res