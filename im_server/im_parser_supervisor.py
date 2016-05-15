#!/usr/bin/python
# -*- coding: utf-8 -*-

import im_masterconfigclass
import json
import logging
import os
import setproctitle
import signal
import socket
import sys
import time
import xmlrpclib

from im_confnagiosparserclass import ConfNagiosParser
from im_dbclass import DBManagement_postgres

from pysvn import Client
from shutil import rmtree, copytree

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import PublishOptions
from autobahn.wamp import auth

class WAMPSub(ApplicationSession):

	def onConnect(self):
		logging.info('WAMPSub connected. joining realm {} as user {} ...'.format(self.config.realm, USER))
		self.join(self.config.realm, [u"wampcra"], USER)

	def onClose(self, wasClean):
		pid = self.config.extra['pid']
		logging.error('WAMPSub connection lost'.format())
		os.kill(pid, signal.SIGTERM)

	def onDisconnect(self):
		pid = self.config.extra['pid']
		logging.error('WAMPSub disconnected'.format())
		os.kill(pid, signal.SIGTERM)

	def onChallenge(self, challenge):
		logging.info('WAMPSub authentication challenge received: {}'.format(challenge))
		if challenge.method == u"wampcra":
			if u'salt' in challenge.extra:
				key = auth.derive_key(PASSWORDS[USER].encode('utf8'),
				challenge.extra['salt'].encode('utf8'),
				challenge.extra.get('iterations', None),
				challenge.extra.get('keylen', None))
			else:
				key = PASSWORDS[USER].encode('utf8')
			signature = auth.compute_wcs(key, challenge.extra['challenge'].encode('utf8'))
			return signature.decode('ascii')
		else:
			raise Exception("don't know how to compute challenge for authmethod {}".format(challenge.method))

	@inlineCallbacks
	def onJoin(self, details):
		logging.info("Session joined WAMPSub")

		def onReceiveMsg(msg):
			parser_request = ''
			parser_ret = {}
			d_agent_info = {}

			parser_ret['topic'] = 'im.supervisor.status.sync'

			logging.debug('Message received : {} on {}'.format(msg, uriTopic))

			try:
				logging.debug('Convert message in Parser request format'.format())
				parser_request = json.loads(msg)

				conf_file_path = parser_request['conf_file_path']
				conf_dir_path = parser_request['conf_dir_path']
				agent_name = parser_request['agent_name']
				
				d_agent_info['agent_name'] = parser_request['agent_name']
				d_agent_info['agent_connection_type'] = parser_request['agent_connection_type']
				d_agent_info['agent_ip'] = parser_request['agent_ip']
				d_agent_info['agent_rpc_port'] = parser_request['agent_rpc_port']
				
				if 'port_ssh_tunnel' in parser_request:
					d_agent_info['port_ssh_tunnel'] = parser_request['port_ssh_tunnel']

				try:
					logging.debug('Remove old "supervisor_{}_latest" tag on SVN {} for {}'.format(agent_name, Conf.svn_server, Conf.svn_repo))
					SVNclient.remove('{}/{}/tags/supervisor_{}_latest'.format(Conf.svn_server, Conf.svn_repo, agent_name))
				except Exception, e:
					logging.warning('Failed to remove "supervisor_{}_latest" tag on SVN {} for {} : {}'.format(agent_name, Conf.svn_server, Conf.svn_repo, e))

				parser_ret['to_publish'] = {'msg': 'Remove old tag in SVN'.format(), 'progress': 11, 'status': 'success'}
				RPC.publish(json.dumps(parser_ret))

				try:
					logging.debug('Init {} repo on {}'.format(Conf.svn_repo, Conf.svn_server))
					SVNclient.import_('/tmp/inman', '{}/{}/trunk'.format(Conf.svn_server, Conf.svn_repo), 'Init repo with initial supervisor conf')
				except Exception, e:
					logging.debug('Repo {} already init on {} : {}'.format(Conf.svn_repo, Conf.svn_server, e))
					logging.debug('Checkout {} repo'.format(Conf.svn_repo))
					SVNclient.checkout('{}/{}/trunk/supervisor/{}'.format(Conf.svn_server, Conf.svn_repo, agent_name), '/tmp/inman/svn/{}'.format(agent_name))
					
					parser_ret['to_publish'] = {'msg': 'Checkout'.format(), 'progress': 12, 'status': 'success'}
					RPC.publish(json.dumps(parser_ret))

					logging.debug('Remove old tree from {} supervisor {}'.format(Conf.svn_repo, agent_name))
					SVNclient.remove('/tmp/inman/svn/{}/etc'.format(agent_name), force=True)
					SVNclient.checkin('/tmp/inman/svn/{}'.format(agent_name), 'New init')

					parser_ret['to_publish'] = {'msg': 'Remove old tree'.format(), 'progress': 13, 'status': 'success'}
					RPC.publish(json.dumps(parser_ret))

					logging.debug('Copy file from last SCP sync {} into repo "/tmp/inman/svn/{}/etc"'.format(conf_dir_path, agent_name))
					copytree('/tmp/inman/supervisor/{}/etc'.format(agent_name), '/tmp/inman/svn/{}/etc'.format(agent_name))
					
					parser_ret['to_publish'] = {'msg': 'Copy SCP file'.format(), 'progress': 14, 'status': 'success'}
					RPC.publish(json.dumps(parser_ret))

					logging.debug('Add and commit the tree'.format())
					SVNclient.add('/tmp/inman/svn/{}/etc'.format(agent_name))
					SVNclient.checkin('/tmp/inman/svn/{}/etc'.format(agent_name), 'New init')

					parser_ret['to_publish'] = {'msg': 'Add new commit tree'.format(), 'progress': 15, 'status': 'success'}
					RPC.publish(json.dumps(parser_ret))

					logging.debug('Delete temp SVN repo for supervisor {}'.format(agent_name))
					rmtree('/tmp/inman/svn/{}'.format(agent_name))

					parser_ret['to_publish'] = {'msg': 'Delete temp SVN repo'.format(), 'progress': 16, 'status': 'success'}
					RPC.publish(json.dumps(parser_ret))
					pass

				logging.debug('Create new tag for {} latest supervisor conf'.format(agent_name))
				SVNclient.copy('{}/{}/trunk/supervisor/{}'.format(Conf.svn_server, Conf.svn_repo, agent_name), '{}/{}/tags/supervisor_{}_latest'.format(Conf.svn_server, Conf.svn_repo, agent_name))	

				parser_ret['to_publish'] = {'msg': 'Create new tag'.format(), 'progress': 17, 'status': 'success'}
				RPC.publish(json.dumps(parser_ret))

			except Exception, e:
				logging.error('Parser failed on : {}'.format(e))
				rmtree('/tmp/inman/supervisor/{}'.format(agent_name))
				parser_ret['to_publish'] = {'msg': 'Parser failed on : {}'.format(e), 'progress': 10, 'status': 'failed'}
				RPC.publish(json.dumps(parser_ret))

			try:
				logging.debug('Parse config {}'.format(conf_file_path))
				
				NagiosConf = ConfNagiosParser(conf_file_path, d_agent_info)
				IMDB_psg = DBManagement_postgres()
				#print NagiosConf.list_resources()
				print NagiosConf.list_command()
				#print NagiosConf.list_check()
				##
				# Insert in DB
				##

				parser_ret['to_publish'] = {'msg': 'Parse config'.format(), 'progress': 20, 'status': 'success'}
				RPC.publish(json.dumps(parser_ret))
			except Exception, e:
				logging.error('Parser failed on : {}'.format(e))
				rmtree('/tmp/inman/supervisor/{}'.format(agent_name))
				parser_ret['to_publish'] = {'msg': 'Parser failed on : {}'.format(e), 'progress': 17, 'status': 'failed'}
				RPC.publish(json.dumps(parser_ret))

		try:
			sub = yield self.subscribe(onReceiveMsg, uriTopic)
			logging.debug('Success subscribed to topic {}'.format(uriTopic))
		except Exception as e:
			logging.error('Could not subscribe to {}: {}'.format(uriTopic, e))

		RPC = self.config.extra['rpcApi']

        # can do subscribes, registers here e.g.:
        # yield self.subscribe(...)
        # yield self.register(...)

def launchWAMPSub(rpcApi):

	pid = os.getpid()

	try:
		logging.info('Launch Parser with launchWAMPSub on {}'.format(urlCrossbar))
		fd = open('/var/run/im/im_parser_websocket_sub_supervisor.pid', 'w')
		fd.write(str(pid))
		fd.close()

		runner = ApplicationRunner(url=u"ws://{0}:{1}/ws".format(urlCrossbar, portCrossbar), realm=realmCrossbar, extra={'pid':pid, 'rpcApi':rpcApi})
		runner.run(WAMPSub)
	except Exception, e:
		logging.error('Parser with launchWAMPSub error : {0}'.format(e))
		os.kill(pid, signal.SIGTERM)
		pass

def get_login (realm, username, may_save):
	logging.info('Login into SVN server {}'.format(urlCrossbar))
	return True, "admin", "Sys.Nepi-vsvn", False

log_message = "delete"
def get_log_message():
	return True, log_message

try:
	setproctitle.setproctitle('IM Parser Supervisor')

	Conf = im_masterconfigclass.ConfObjClass('im_master.cfg', 'im_master_confcheck.cfg')

	logParser = Conf.parser_log_file
	
	if not os.path.isfile(logParser):
		path, filename = os.path.split(logParser)
		try:
			os.makedirs(path)
		except Exception, e:
			pass
		open(logParser, 'a').close()

	logging.basicConfig(level=eval(Conf.log_debug_level), filename=logParser, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

	logging.info('Init Parser with launchWAMPSub'.format())

	PASSWORDS = {
		unicode(Conf.websocket_user): unicode(Conf.websocket_pass)
	}

	USER = unicode(Conf.websocket_user)

	urlCrossbar = Conf.websocket_router
	portCrossbar = Conf.websocket_port
	realmCrossbar = unicode(Conf.websocket_realm)
	uriTopic = unicode(Conf.websocket_uriparser)

	SVNclient = Client()
	SVNclient.callback_get_login = get_login
	SVNclient.callback_get_log_message = get_log_message

	rpcApi = xmlrpclib.ServerProxy('http://127.0.0.1:{}'.format(Conf.master_rpc_wpub_port), allow_none=True)

	launchWAMPSub(rpcApi)

except Exception, e:
	logging.error('Failed to init Parser with WAMP : {}'.format(e))
	sys.exit()

