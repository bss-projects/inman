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

from multiprocessing import Process, Queue
from SimpleXMLRPCServer import SimpleXMLRPCServer

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import PublishOptions
from autobahn.wamp import auth

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
		server = self.config.extra['server']

		while True:

			server.handle_request()
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

def launchWAMPPub(queue, server):

	pid = os.getpid()

	try:
		logging.info('Launch RPC with launchWAMPPub on {}'.format(urlCrossbar))
		fd = open('/var/run/im/im_rpc_websocket_pub_supervisor.pid', 'w')
		fd.write(str(pid))
		fd.close()

		runner = ApplicationRunner(url=u"ws://{0}:{1}/ws".format(urlCrossbar, portCrossbar), realm=realmCrossbar, extra={'queue':queue, 'pid':pid, 'server':server})
		runner.run(WAMPPub)
	except Exception, e:
		logging.error('RPC with launchWAMPPub error : {0}'.format(e))
		os.kill(pid, signal.SIGTERM)
		pass

def publish(message):
	global q

	try:
		logging.debug('Send message for publishing on WAMP : {}'.format(message))
		q.put(message)
	except Exception, e:
		logging.warning('Failed to send message for WAMP : {}'.format(e))
	

try:
	setproctitle.setproctitle('IM RPC WPub Supervisor')

	Conf = im_masterconfigclass.ConfObjClass('im_master.cfg', 'im_master_confcheck.cfg')

	logRPC = Conf.rpc_log_file
	
	if not os.path.isfile(logRPC):
		path, filename = os.path.split(logRPC)
		try:
			os.makedirs(path)
		except Exception, e:
			pass
		open(logRPC, 'a').close()

	logging.basicConfig(level=eval(Conf.log_debug_level), filename=logRPC, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

	logging.info('Init RPC for WPub'.format())

	PASSWORDS = {
		unicode(Conf.websocket_user): unicode(Conf.websocket_pass)
	}

	USER = unicode(Conf.websocket_user)

	urlCrossbar = Conf.websocket_router
	portCrossbar = Conf.websocket_port
	realmCrossbar = unicode(Conf.websocket_realm)

	server = SimpleXMLRPCServer(('0.0.0.0', Conf.master_rpc_wpub_port), logRequests=True, allow_none=True)
	server.register_function(publish)
	
	q = Queue()

	pWPub = Process(target=launchWAMPPub, args=(q,server,))
	pWPub.start()

##	server.serve_forever()

	while True:
		if not pWPub.is_alive() :
			try:
				pWPub.terminate()

				if pWPub.is_alive():
					logging.warning('Process pWPub alive'.format())
					os.kill(pWPub.pid, signal.SIGKILL)
					logging.warning('Process pWPub killed : {0}'.format(pWSub.exitcode))


				if DoesServiceExist(urlCrossbar, portCrossbar) and not pWPub.is_alive() :
					q = Queue()
					logging.warning('Process pWPub was kill before restart ? : {0}'.format(pWPub.exitcode))
					logging.info('Start pWPub process'.format())
					pWPub = Process(target=launchWAMPPub, args=(q,))
					pWPub.start()

				elif not DoesServiceExist(urlCrossbar, portCrossbar):
					logging.error('Connection to websocket router {0}:{1} Failed'.format(urlCrossbar, portCrossbar))
				else :
					logging.error('pWPub : {0}'.format(pWPub.is_alive()))

			except Exception,e:
				logging.error('Process error : {0}'.format(e))
				pWPub.terminate()
				sys.exit()
		time.sleep(5.0)

except Exception, e:
	logging.error('Failed to init RPC for WPub : {}'.format(e))
	pWPub.terminate()
	sys.exit()
	raise e