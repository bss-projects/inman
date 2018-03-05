#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# Need since v0.9.3-RC1
####

#~~~~~~~~~~~~~~~~~
# This script have to be laucnh every day at 23:59 by CRONTAB
# This script is made to detect user account expired but also
# send mail before expiration to alert
#~~~~~~~~~~~~~~~~~

import email
import email.header
import email.message
import html2text
import json
import logging
import os
import psycopg2
import smtplib
import sys
import time

from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, Template

# SELECT * FROM users_freeradius WHERE (user_info->'expiration_timestamp') IS NOT NULL AND CAST(user_info->>'expiration_timestamp' AS FLOAT) - 1529272800  < 2628000

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

def send_mail(msg, radiusname):
	print 'sendmail'
	To = []
	s = smtplib.SMTP(Conf['Radius'][radiusname]['mail_smtp_server'])
	print msg['Cc']
	if msg['Cc'] != None:
		To.append(msg['To'])
		l_cc = msg['Cc'].split(',')
		for cc_mail in l_cc:
			To.append(cc_mail) 
	else:
		To.append(msg['To'])

	print 'To: {0}'.format(To)
	s.sendmail(msg['From'], To, msg.as_string())
	s.quit()

def setup_mail(d_one_month, d_one_week, d_one_day, l_radiusname):
	env = Environment(loader=FileSystemLoader('./'), extensions=['jinja2.ext.i18n'])

	for radiusname in l_radiusname:
		if radiusname in d_one_month.keys():
			l_one_month = d_one_month[radiusname]
		else:
			l_one_month = []

		if radiusname in d_one_week.keys():
			l_one_week = d_one_week[radiusname]
		else:
			l_one_week = []

		if radiusname in d_one_day.keys():
			l_one_day = d_one_day[radiusname]
		else:
			l_one_day = []

		d_render = {'l_one_month': l_one_month, 'l_one_week': l_one_week, 'l_one_day': l_one_day}
		OTemplate = env.get_template('im_cron_expiration_user_mail_template_freeradius.tpl')

		html_body = OTemplate.render(d_render)

		new = MIMEMultipart("mixed")
		body = MIMEMultipart("alternative")
		body.attach( MIMEText('{0}'.format(html2text.html2text(html_body)), "plain") )
		body.attach( MIMEText(html_body, "html") )
		new.attach(body)

		new['From'] = Conf['Radius'][radiusname]['mail_sender']
		new['Subject'] = '{0} - {1}'.format(Conf['Radius'][radiusname]['mail_subject'], radiusname)
		new['To'] = Conf['Radius'][radiusname]['mail_destination']

		send_mail(new, radiusname)

		logging.debug('Mail to {0} for {1}'.format(new['To'], new['Subject']))

doc = {}
doc_user_trace_action = {}
d_search_options = {}
l_one_month = []
l_one_week = []
l_one_day = []
l_expired = []

l_radiusname = []

d_one_month = {}
d_one_week = {}
d_one_day = {}
d_expired = {}

to_insert = ''

with open('im_cron_conf_expiration_user.cfg') as data_file:
	Conf = json.load(data_file)

if not os.path.isfile(Conf['Log']['file']):
		path, filename = os.path.split(Conf['Log']['file'])
		os.makedirs(path)
		open(Conf['Log']['file'], 'a').close()
logging.basicConfig(level=eval(Conf['Log']['debug_level']), filename=Conf['Log']['file'], format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

try:
	logging.debug('Connect to DB {0} on {1}'.format(Conf['Database']['database_name'], Conf['Database']['database_host']))
	IMDB = DBManagement(host=Conf['Database']['database_host'], database=Conf['Database']['database_name'], user=Conf['Database']['database_user'], password=Conf['Database']['database_pass'], port=Conf['Database']['database_port'])

	current_timestamp = time.time()

	d_search_options['fields'] = 'id, user_info, CAST(user_info->>\'expiration_timestamp\' AS FLOAT) - {0} AS expiration_delay'.format(current_timestamp)
	d_search_options['filter'] = '(user_info->\'expiration_timestamp\') IS NOT NULL AND CAST(user_info->>\'expiration_timestamp\' AS FLOAT) - {0}  < 2628000 AND user_info->>\'expiration_status\' = \'ok\''.format(current_timestamp)

	l_results = IMDB.search(collection='users_freeradius', search_parameter=d_search_options)
except Exception, e:
	logging.error('Failed to connect DB {0} on {1}: {2}'.format(Conf['Database']['database_name'], Conf['Database']['database_host'], e))
	raise e


print 2628000 - 86400 / 2
print 2628000 + 86400 / 2

print 604800 - 86400 / 2
print 604800 + 86400 / 2

print 86400 - 86400 / 2
print 86400 + 86400 / 2

if l_results :
	for result in l_results:
		user_id = result[0]
		user_info = result[1]
		expiration_delay = result[2]
		radiusname = user_info['radiusname']

		if radiusname not in l_radiusname:
			l_radiusname.append(radiusname)

		print expiration_delay

		if expiration_delay >= 2628000 - 86400 / 2 and expiration_delay <= 2628000 + 86400 / 2:
			l_one_month.append(user_info)
			if radiusname not in d_one_month.keys():
				d_one_month[radiusname] = [user_info]
			else:
				d_one_month[radiusname].append(user_info)
		elif expiration_delay >= 604800 - 86400 / 2 and expiration_delay <= 604800 + 86400 / 2:
			l_one_week.append(user_info)
			if radiusname not in d_one_week.keys():
				d_one_week[radiusname] = [user_info]
			else:
				d_one_week[radiusname].append(user_info)
		elif expiration_delay >= 0 and expiration_delay <= 86400 + 86400 / 2:
			l_one_day.append(user_info)
			if radiusname not in d_one_day.keys():
				d_one_day[radiusname] = [user_info]
			else:
				d_one_day[radiusname].append(user_info)
		elif expiration_delay < 0:
			l_expired.append(user_info)
			if radiusname not in d_expired.keys():
				d_expired[radiusname] = [{'user_id': user_id, 'user_info': user_info}]
			else:
				d_expired[radiusname].append({'user_id': user_id, 'user_info': user_info})
else:
	logging.debug('No user concerne by expiration protocol DB {0} on {1}'.format(Conf['Database']['database_name'], Conf['Database']['database_host']))

print d_one_month
print d_one_week
print d_one_day
print d_expired

if (len(d_one_month) != 0) or (len(d_one_week) != 0) or (len(d_one_day) != 0):
	try:
		setup_mail(d_one_month, d_one_week, d_one_day, l_radiusname)
	except Exception, e:
		logging.error('Failed to send mail about user account expiration : {0}'.format(e))

for radiusname in l_radiusname:
	if radiusname in d_expired.keys():
		for user in d_expired[radiusname]:
			user_id = user['user_id']
			user_info = user['user_info']
			user_trace = {}

			user_info['expiration_status'] = 'exp.'

			logging.debug('User {0} expire on {1} for {2}'.format(user_info['username'], user_info['expiration_date'], radiusname))	

			to_insert = json.dumps(user_info).replace('\'', '\'\'')

			doc['user_info'] = to_insert

			d_search_options['fields'] = ''
			d_search_options['filter'] = 'id = {0}'.format(user_id)

			IMDB.update('users_freeradius', doc, search_parameter=d_search_options)

			user_trace['plugin'] = 'Freeradius'
			user_trace['agent'] = radiusname
			user_trace['date'] = current_timestamp
			user_trace['action'] = 'Account expired'
			user_trace['login'] = 'CRON'
			user_trace['action_data'] = doc['user_info']

			to_insert = json.dumps(user_trace).replace('\'', '\'\'')
			doc_user_trace_action['user_trace_action_info'] = to_insert

			IMDB.publish('user_trace_action', doc_user_trace_action)