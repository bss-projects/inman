#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from os import fsync
from subprocess import call

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
				d_block_info['rangename'] = d_block_info['ip']

			logging.debug('Add spec client block in {} for {}'.format(self.filename, d_block_info['subnet']))
			self.l_block.append('client {}\n \
{{\n \
	ipaddr = {}\n \
	secret = {}\n \
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
		try:
			logging.info('Restart Freeradius'.format())
			service = call(['/etc/init.d/freeradius', 'restart', '>', 'monitoring_restart.log'])
		except Exception, e:
			logging.error('Failed to restart Freeradius "{}" : {}'.format(service, e))