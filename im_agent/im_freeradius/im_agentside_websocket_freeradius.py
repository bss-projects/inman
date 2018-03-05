#!/usr/bin/python

__all__ = ('follow',)

import im_agentconfigclass_freeradius
import logging
import os
import re
import setproctitle
import signal
import socket
import sys
import time

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import PublishOptions
from autobahn.wamp import auth

from multiprocessing import Process, Queue

class LogRotateSigHup(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class FileLog(ApplicationSession):

	def onConnect(self):
		logging.info('FileLog connected. joining realm {} as user {} ...'.format(self.config.realm, USER))
		self.join(self.config.realm, [u"wampcra"], USER)

	def onClose(self, wasClean):
		pid = self.config.extra['pid']
		logging.error('File log connection lost'.format())
		os.kill(pid, signal.SIGTERM)

	def onDisconnect(self):
		pid = self.config.extra['pid']
		logging.error('File log disconnected'.format())
		os.kill(pid, signal.SIGTERM)

	def onChallenge(self, challenge):
		logging.info('File log authentication challenge received: {}'.format(challenge))
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
		logging.info('session joined FileLog')

		def time_sorted_ls(radiusname, file=None, path=None):

			if radius_agent_name != radiusname:
				return list()

			if file == None:
				file = logRadius

			if path == None and file != None:
				path = os.path.dirname(os.path.realpath(file))

			list_dir = os.listdir(path)

			filter_func = lambda file: re.search('(radius\.log)([\.0-9]*)(?!gz)$', file, re.IGNORECASE)
			list_dir_filter = filter(filter_func, list_dir)

			mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
			return list(sorted(list_dir_filter, key=mtime))

		def readLogFreeradius(radiusname, file):
			ret = ''

			if radius_agent_name != radiusname:
				return ret

			path = os.path.dirname(os.path.realpath(logRadius))

			with open('{0}/{1}'.format(path, file), 'rt') as f:
				for line in f:
					ret += '{0}</br>'.format(line)

			return ret

		try:
			reg_read = yield self.register(readLogFreeradius, uriRPC_readfile_log)
			reg_list = yield self.register(time_sorted_ls, uriRPC_listfile_log)
			logging.info('Procedure to read Radius file log registered')
		except Exception as e: 
			logging.error('Could not register procedure: {0}'.format(e))

        # can do subscribes, registers here e.g.:
        # yield self.subscribe(...)
        # yield self.register(...)

def launchFilelog():

	pid = os.getpid()

	try:
		if not os.path.isfile('/var/run/im/im_agent_websocket_rpc_freeradius.pid'):
			path, filename = os.path.split('/var/run/im/im_agent_websocket_rpc_freeradius.pid')
			if not os.path.isdir(path):
				os.makedirs(path)
			open('/var/run/im/im_agent_websocket_rpc_freeradius.pid', 'a').close()

		fd = open('/var/run/im/im_agent_websocket_rpc_freeradius.pid', 'w')
		fd.write(str(pid))
		fd.close()

		runner = ApplicationRunner(url=u"ws://{0}:{1}/ws".format(urlCrossbar, portCrossbar), realm=realmCrossbar, extra={'pid':pid})
		runner.run(FileLog)
	except Exception, e:
		logging.error('launchFilelog error : {0}'.format(e))
		os.kill(pid, signal.SIGTERM)
		pass

class LiveLog(ApplicationSession):

	def onConnect(self):
		logging.info('LiveLog connected. joining realm {} as user {} ...'.format(self.config.realm, USER))
		self.join(self.config.realm, [u"wampcra"], USER)

	def onClose(self, wasClean):
		pid = self.config.extra['pid']
		logging.error('Live log connection lost'.format())
		os.kill(pid, signal.SIGTERM)

	def onDisconnect(self):
		pid = self.config.extra['pid']
		logging.error('Live log disconnected'.format())
		os.kill(pid, signal.SIGTERM)

	def onChallenge(self, challenge):
		logging.info('Live log authentication challenge received: {}'.format(challenge))
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
		logging.info("session joined LiveLog")

		queue = self.config.extra['queue']
		radius_agent_name = self.config.extra['radius_agent_name']

		while True:

			to_publish = queue.get()
			logging.debug('To publish : {0}'.format(to_publish))
			try:
				yield self.publish(uriTopic, [radius_agent_name, to_publish], options = PublishOptions(acknowledge = True))
				logging.debug('ok, event published to topic'.format())
			except Exception as e:
				logging.error('publication to topic failed: {0}'.format(e))

        # can do subscribes, registers here e.g.:
        # yield self.subscribe(...)
        # yield self.register(...)

def launchLivelog(queue, radius_agent_name):

	pid = os.getpid()

	try:
		if not os.path.isfile('/var/run/im/im_agent_websocket_live_freeradius.pid'):
			path, filename = os.path.split('/var/run/im/im_agent_websocket_live_freeradius.pid')
			if not os.path.isdir(path):
				os.makedirs(path)
			open('/var/run/im/im_agent_websocket_live_freeradius.pid', 'a').close()

		fd = open('/var/run/im/im_agent_websocket_live_freeradius.pid', 'w')
		fd.write(str(pid))
		fd.close()

		runner = ApplicationRunner(url=u"ws://{0}:{1}/ws".format(urlCrossbar, portCrossbar), realm=realmCrossbar, extra={'queue':queue, 'pid':pid, 'radius_agent_name':radius_agent_name})
		runner.run(LiveLog)
	except Exception, e:
		logging.error('launchLivelog error : {0}'.format(e))
		os.kill(pid, signal.SIGTERM)
		pass

def follow(stream):
	"Follow the live contents of a text file."
	line = ''
	for block in iter(lambda:stream.read(1024), None):
		if '\n' in block:
            # Only enter this block if we have at least one line to yield.
            # The +[''] part is to catch the corner case of when a block
            # ends in a newline, in which case it would repeat a line.
			for line in (line+block).splitlines(True)+['']:
				if line.endswith('\n'):
					yield line
            # When exiting the for loop, 'line' has any remaninig text.
		elif not block:
            # Wait for data.
			time.sleep(1.0)
    # The End.

def streamfile(q):
	logging.info("Streaming Radius log file ready")

	pid = os.getpid()

	try:
		if not os.path.isfile('/var/run/im/im_agent_streamfile_freeradius.pid'):
			path, filename = os.path.split('/var/run/im/im_agent_streamfile_freeradius.pid')
			if not os.path.isdir(path):
				os.makedirs(path)
			open('/var/run/im/im_agent_streamfile_freeradius.pid', 'a').close()

		fd = open('/var/run/im/im_agent_streamfile_freeradius.pid', 'w')
		fd.write(str(pid))
		fd.close()
		signal.signal(signal.SIGHUP, signal_logrotate)
	except Exception, e:
		logging.error('Receive exception in Init streaming logfile process : {}'.format(e))
		raise e

	while True:
		try:
			with open(logRadius, 'rt') as following:
				logging.debug('Open log file {0} to stream: {1}'.format(logRadius, following))
				following.seek(0, 2)
				for line in follow(following):
					logging.debug('Send from stream : {0}'.format(line))
					q.put(line)
		except LogRotateSigHup as e:
			logging.info('Receive Logrotate event : {0}'.format(e))
			following.close()
		except Exception, e:
			logging.error('Receive exception during streaming logfile : {0}'.format(e))
			raise e
			break

def signal_logrotate(signum, stack):
	logging.debug('Receive SIGHUP from Logrotate')
	raise LogRotateSigHup('Receive SIGHUP from Logrotate')

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

if __name__ == '__main__':
    # As a simple demonstration, run it with the filename to tail.
	setproctitle.setproctitle('IM Websocket Freeradius')

	Conf = im_agentconfigclass_freeradius.ConfObjClass('im_agent_freeradius.cfg', 'im_agent_freeradius_confcheck.cfg')
	
	if not os.path.isfile(Conf.log_file):
		path, filename = os.path.split(Conf.log_file)
		if not os.path.isdir(path):
			os.makedirs(path)
		open(Conf.log_file, 'a').close()
	
	logging.basicConfig(level=eval(Conf.websocket_debug_level), filename=Conf.websocket_log_file, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')


	PASSWORDS = {
		unicode(Conf.websocket_user): unicode(Conf.websocket_pass)
	}

	USER = unicode(Conf.websocket_user)

	urlCrossbar = Conf.websocket_router
	portCrossbar = Conf.websocket_port
	realmCrossbar = unicode(Conf.websocket_realm)
	uriTopic = unicode(Conf.websocket_uripubsub)
	uriRPC_readfile_log = unicode(Conf.websocket_urirpc_readfile_log)
	uriRPC_listfile_log = unicode(Conf.websocket_urirpc_listfile_log)
	logRadius = Conf.websocket_radius_log
	radius_agent_name = Conf.agent_name

	q = Queue()
	pLive = Process(target=launchLivelog, args=(q,radius_agent_name,))
	pFile = Process(target=launchFilelog)
	pStream = Process(target=streamfile, args=(q,))
	pLive.start()
	pFile.start()
	pStream.start()

	while True:
		try:
			if not pFile.is_alive() or not pLive.is_alive() or not pStream.is_alive():
				try:
					pLive.terminate()
					pFile.terminate()
					pStream.terminate()

					if pLive.is_alive():
						logging.warning('Process pLive alive'.format())
						os.kill(pLive.pid, signal.SIGKILL)
						logging.warning('Process pLive killed : {0}'.format(pLive.exitcode))
					if pFile.is_alive():
						logging.warning('Process pFile alive'.format())
						os.kill(pFile.pid, signal.SIGKILL)
						logging.warning('Process pFile killed : {0}'.format(pFile.exitcode))
					if pStream.is_alive():
						logging.warning('Process pStream alive'.format())
						os.kill(pStream.pid, signal.SIGKILL)
						logging.warning('Process pStream killed : {0}'.format(pStream.exitcode))


					if DoesServiceExist(urlCrossbar, portCrossbar) and not pLive.is_alive() and not pFile.is_alive() and  not pStream.is_alive():
						q = Queue()
						logging.warning('Process pLive was kill before restart ? : {0}'.format(pLive.exitcode))
						logging.info('Start pLive process'.format())
						pLive = Process(target=launchLivelog, args=(q,radius_agent_name,))
						pLive.start()

						logging.warning('Process pFile was kill before restart ? : {0}'.format(pFile.exitcode))
						logging.info('Start pFile process'.format())
						pFile = Process(target=launchFilelog)
						pFile.start()

						logging.warning('Process pStream was kill before restart ? : {0}'.format(pStream.exitcode))
						logging.info('Start pStream process'.format())
						pStream = Process(target=streamfile, args=(q,))
						pStream.start()
					elif not DoesServiceExist(urlCrossbar, portCrossbar):
						logging.error('Connection to websocket router {0}:{1} Failed'.format(urlCrossbar, portCrossbar))
					else :
						logging.error('pLive : {0} / pFile : {1} / pStream : {2}'.format(pLive.is_alive(), pFile.is_alive(), pStream.is_alive()))

				except Exception,e:
					logging.error('Process error : {0}'.format(e))
					pLive.terminate()
					pFile.terminate()
					pStream.terminate()
					sys.exit()
			time.sleep(5.0)

		except Exception,e:
			logging.error('{0}'.format(e))
			pLive.terminate()
			pFile.terminate()
			pStream.terminate()
			sys.exit()
