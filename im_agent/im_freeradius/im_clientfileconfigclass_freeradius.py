#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from os import fsync
from subprocess import call, Popen, PIPE

class ParseConfRadiusClient(object):
	"""docstring for ParseConfRadiusClient"""
	def __init__(self, filename, filepath):
		super(ParseConfRadiusClient, self).__init__()
		self.filename = filename
		self.filepath = filepath
		self.complete_filepathname = '{}/{}'.format(filepath,filename)
		self.l_block = []
		self.blocktype = 'client'
		self.fd = None

	def add_block(self, d_block_info=None):
		try:
			if 'ip' in d_block_info:
				d_block_info['subnet'] = d_block_info['ip']
				d_block_info['rangename'] = '{0}-{1}'.format(d_block_info['name'].replace(' ', '-'), d_block_info['ip'])

			logging.debug('Add spec client block in {} for {}'.format(self.filename, d_block_info['subnet']))
			self.l_block.append('client {} {{\n \
	ipaddr = {}\n\
	secret = {}\n\
}}\n\n'.format(d_block_info['rangename'], d_block_info['subnet'], d_block_info['sharedsecret']))
		except Exception, e:
			logging.warning('Failed to add spec client block in {} for {} : {}'.format(self.filename, d_block_info['subnet'], e))
		

	def delete_block(self, d_block_info=None):
		pass

	def edit_block(self, d_block_info=None):
		pass

	def get_blocks(self):
		return self.l_block

	def commit_blocks(self):
		try:
			logging.debug('Open "{}" to write block'.format(self.filename))			
			self.fd = open(self.complete_filepathname, 'w')

			logging.debug('Write client block in {}'.format(self.filename))
			for block in self.l_block:
				logging.debug('Block to write : {}'.format(block))
				self.fd.write('{}'.format(block))
			self.fd.flush()
			fsync(self.fd)

			logging.debug('Close "{}" after writing block'.format(self.filename))
			self.fd.close()
			self.l_block = []
		except Exception, e:
			self.fd.close()
			self.l_block = []
			logging.warning('Failed to write client block in {} : {}'.format(self.filename, e))

	def restart_freeradius(self):
		service = ''
		stdout = ''
		stderrno = ''
		
		try:
			logging.info('Restart Freeradius'.format())
			## For Init.D Style
#			sp = Popen(['/etc/init.d/freeradius', 'restart', '>', 'monitoring_restart.log'], stdout=PIPE, stderr=PIPE) 
			## For systemctl Style
			sp = Popen(['systemctl restart radiusd'], shell=True, stdout=PIPE, stderr=PIPE)
			stdout, stderrno = sp.communicate()

#			if out:
#				print "standard output of subprocess:"
#				print out
#			if errno:
#				print "standard error of subprocess:"
#				print err
#			print "returncode of subprocess:"
#			print sp.returncode

#			service = call(['/etc/init.d/freeradius', 'restart', '>', 'monitoring_restart.log'])
#			logging.info('Freeradius restarting : {0}'.format(service))

			if sp.returncode != 0:
				logging.error('Failed to restart Freeradius\n Output : {0}\n Errno : {1}'.format(stdout, stderrno))
		except Exception, e:
			logging.error('Failed to restart Freeradius "{}" : {}'.format(service, e))