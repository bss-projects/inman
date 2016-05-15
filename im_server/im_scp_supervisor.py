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

from multiprocessing import Process, Queue

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import PublishOptions
from autobahn.wamp import auth

from paramiko import SSHClient
from scp import SCPClient


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
			scp_request = ''
			scp_ret = {}
			scp_to_parser = {}

			scp_ret['topic'] = 'im.supervisor.status.sync'
			scp_to_parser['topic'] = 'im.supervisor.parser'

			logging.debug('Message received : {} on {}'.format(msg, uriTopic))

			try:
				logging.debug('Convert message in SCP request format'.format())
				scp_request = json.loads(msg)

				scp_ret['to_publish'] = {'msg': 'Init SSH success from {} on {}'.format(scp_request['hostname'], scp_request['agent_name']), 'progress': 2, 'status': 'success'}

				#queue.put(json.dumps(scp_ret))
				RPC.publish(json.dumps(scp_ret))

				logging.debug('Init SSH connection for SCP on {}'.format(scp_request['hostname']))
				ssh = SSHClient()
				ssh.load_system_host_keys()
				ssh.connect(scp_request['hostname'])

				logging.debug('Init SCP on {}'.format(scp_request['hostname']))
				scp = SCPClient(ssh.get_transport())
				scp_ret['to_publish'] = {'msg': 'Init SCP success from {} on {}'.format(scp_request['hostname'], scp_request['agent_name']), 'progress': 4, 'status': 'success'}

				#queue.put(json.dumps(scp_ret))
				RPC.publish(json.dumps(scp_ret))

				scp_tmp_conf_dir_path = '/tmp/inman/supervisor/{}'.format(scp_request['agent_name'])
				scp_tmp_conf_file_path = '/tmp/inman/supervisor/{}/etc/{}'.format(scp_request['agent_name'], scp_request['conf_file'])

				if not os.path.isdir(scp_tmp_conf_dir_path):
					logging.debug('TMP "{}" path does not exist. Try to create'.format(scp_tmp_conf_dir_path))
					os.makedirs(scp_tmp_conf_dir_path)
					logging.debug('Path "{}" created to temporarly storage'.format(scp_tmp_conf_dir_path))

				scp_ret['to_publish'] = {'msg': 'Launch SCP from {} on {}'.format(scp_request['hostname'], scp_request['agent_name']), 'progress': 6, 'status': 'success'}

				#queue.put(json.dumps(scp_ret))
				RPC.publish(json.dumps(scp_ret))

				logging.debug('Launch SCP on {}'.format(scp_request['hostname']))
				scp.get(scp_request['distant_path_conf'], local_path=scp_tmp_conf_dir_path, recursive=True, preserve_times=True)
				#scp.get('/appli/shinken/etc', local_path='/tmp/shinken/', recursive=True, preserve_times=True)

				logging.debug('Close SCP and SSH on {}'.format(scp_request['hostname']))
				scp.close()

				####
				## Put in queue message pour dire que le SCP est finit et qu'il parser et SVN
				####
				scp_ret['to_publish'] = {'msg': 'SCP success from {} on {}'.format(scp_request['hostname'], scp_request['agent_name']), 'progress': 10, 'status': 'success'}
				#queue.put(json.dumps(scp_ret))
				logging.debug('Send progress : {}'.format(scp_ret['to_publish']))
				RPC.publish(json.dumps(scp_ret))

				scp_to_parser['to_publish'] = {'conf_dir_path': scp_tmp_conf_dir_path, 'agent_name' : scp_request['agent_name'], 'conf_file_path': scp_tmp_conf_file_path, 'agent_connection_type' : scp_request['agent_connection_type'], 'agent_ip' : scp_request['agent_ip'], 'agent_rpc_port' : scp_request['agent_rpc_port']}
				logging.debug('Send message to parser : {}'.format(scp_to_parser['to_publish']))
				#queue.put(json.dumps(scp_to_parser))
				RPC.publish(json.dumps(scp_to_parser))

			except Exception, e:
				logging.error('SCP failed on {} : {}'.format(scp_request['hostname'], e))
				scp_ret['to_publish'] = {'msg': 'SCP failed on {} : {}'.format(scp_request['hostname'], e), 'progress': 10, 'status': 'failed'}
				#queue.put(json.dumps(scp_ret))
				RPC.publish(json.dumps(scp_ret))

		try:
			sub = yield self.subscribe(onReceiveMsg, uriTopic)
			logging.debug("Success subscribed to topic {}".format(uriTopic))
		except Exception as e:
			logging.error("Could not subscribe to {}: {}".format(uriTopic, e))

		queue = self.config.extra['queue']
		RPC = self.config.extra['rpcApi']

        # can do subscribes, registers here e.g.:
        # yield self.subscribe(...)
        # yield self.register(...)






class WAMPPub(ApplicationSession):

	def onConnect(self):
		logging.info('WAMPPub connected. joining realm {} as user {} ...'.format(self.config.realm, USER))
		self.join(self.config.realm, [u"wampcra"], USER)

	def onClose(self, wasClean):
		pid = self.config.extra['pid']
		logging.error('WAMPPub connection lost'.format())
		os.kill(pid, signal.SIGTERM)

	def onDisconnect(self):
		pid = self.config.extra['pid']
		logging.error('WAMPPub disconnected'.format())
		os.kill(pid, signal.SIGTERM)

	def onChallenge(self, challenge):
		logging.info('WAMPPub authentication challenge received: {}'.format(challenge))
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
		logging.info("session joined WAMPPub")

		queue = self.config.extra['queue']

		while True:

			msg_received = queue.get()
			logging.debug('Message received : {0}'.format(msg_received))
			try:
				d_to_publish = json.loads(msg_received)
				yield self.publish(d_to_publish['topic'], json.dumps(d_to_publish['to_publish']), options = PublishOptions(acknowledge = True))
				logging.debug('ok, event published to topic {}'.format(d_to_publish['topic']))
			except Exception as e:
				logging.error('publication to topic failed: {}'.format(e))

        # can do subscribes, registers here e.g.:
        # yield self.subscribe(...)
        # yield self.register(...)








def DoesServiceExist(host, port):
	captive_dns_addr = ''
	host_addr = ''

	try:
		captive_dns_addr = socket.gethostbyname('BlahThisDomaynDontExist22.com')
	except:
		pass

	try:
		host_addr = socket.gethostbyname(host)

		if (captive_dns_addr == host_addr):
			return False

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		s.connect((host, port))
		s.close()
	except:
		return False

	return True

def launchWAMPPub(queue):

	pid = os.getpid()

	try:
		logging.info('Launch SCP with launchWAMPPub on {}'.format(urlCrossbar))
		fd = open('/var/run/im/im_scp_websocket_pub_supervisor.pid', 'w')
		fd.write(str(pid))
		fd.close()

		runner = ApplicationRunner(url=u"ws://{0}:{1}/ws".format(urlCrossbar, portCrossbar), realm=realmCrossbar, extra={'queue':queue, 'pid':pid})
		runner.run(WAMPPub)
	except Exception, e:
		logging.error('SCP with launchWAMPPub error : {0}'.format(e))
		os.kill(pid, signal.SIGTERM)
		pass


def launchWAMPSub(queue, rpcApi):

	pid = os.getpid()

	try:
		logging.info('Launch SCP with launchWAMPSub on {}'.format(urlCrossbar))
		fd = open('/var/run/im/im_scp_websocket_sub_supervisor.pid', 'w')
		fd.write(str(pid))
		fd.close()

		runner = ApplicationRunner(url=u"ws://{0}:{1}/ws".format(urlCrossbar, portCrossbar), realm=realmCrossbar, extra={'queue':queue, 'pid':pid, 'rpcApi':rpcApi})
		runner.run(WAMPSub)
	except Exception, e:
		logging.error('SCP with launchWAMPSub error : {0}'.format(e))
		os.kill(pid, signal.SIGTERM)
		pass

try:
	setproctitle.setproctitle('IM SCP Supervisor')

	Conf = im_masterconfigclass.ConfObjClass('im_master.cfg', 'im_master_confcheck.cfg')

	logSCP = Conf.scp_log_file
	
	if not os.path.isfile(logSCP):
		path, filename = os.path.split(logSCP)
		try:
			os.makedirs(path)
		except Exception, e:
			pass
		open(logSCP, 'a').close()

	logging.basicConfig(level=eval(Conf.log_debug_level), filename=logSCP, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

	logging.info('Init SCP with launchWAMPSub'.format())

	PASSWORDS = {
		unicode(Conf.websocket_user): unicode(Conf.websocket_pass)
	}

	USER = unicode(Conf.websocket_user)

	urlCrossbar = Conf.websocket_router
	portCrossbar = Conf.websocket_port
	realmCrossbar = unicode(Conf.websocket_realm)
	uriTopic = unicode(Conf.websocket_uriscp)
	
	q = Queue()
	rpcApi = xmlrpclib.ServerProxy('http://127.0.0.1:{}'.format(Conf.master_rpc_wpub_port), allow_none=True)

	pWSub = Process(target=launchWAMPSub, args=(q,rpcApi,))
	pWSub.start()
	pWPub = Process(target=launchWAMPPub, args=(q,))
	pWPub.start()

	while True:
		if not pWPub.is_alive() or not pWSub.is_alive():
			try:
				pWPub.terminate()
				pWSub.terminate()

				if pWPub.is_alive():
					logging.warning('Process pWPub alive'.format())
					os.kill(pWPub.pid, signal.SIGKILL)
					logging.warning('Process pWPub killed : {0}'.format(pWSub.exitcode))
				if pWSub.is_alive():
					logging.warning('Process pWSub alive'.format())
					os.kill(pWSub.pid, signal.SIGKILL)
					logging.warning('Process pWSub killed : {0}'.format(pWSub.exitcode))


				if DoesServiceExist(urlCrossbar, portCrossbar) and not pWPub.is_alive() and not pWSub.is_alive():
					q = Queue()
					logging.warning('Process pWPub was kill before restart ? : {0}'.format(pWPub.exitcode))
					logging.info('Start pWPub process'.format())
					pWPub = Process(target=launchWAMPPub, args=(q,))
					pWPub.start()

					logging.warning('Process pWSub was kill before restart ? : {0}'.format(pWSub.exitcode))
					logging.info('Start pWSub process'.format())
					pWSub = Process(target=launchWAMPSub, args=(q,))
					pWSub.start()

				elif not DoesServiceExist(urlCrossbar, portCrossbar):
					logging.error('Connection to websocket router {0}:{1} Failed'.format(urlCrossbar, portCrossbar))
				else :
					logging.error('pWPub : {0}'.format(pWPub.is_alive()))

			except Exception,e:
				logging.error('Process error : {0}'.format(e))
				pWPub.terminate()
				pWSub.terminate()
				sys.exit()
		time.sleep(5.0)

except Exception, e:
	logging.error('Failed to init SCP with WAMP : {}'.format(e))
	pWPub.terminate()
	pWSub.terminate()
	sys.exit()
	raise e
