#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from asciimatics.event import Event, KeyboardEvent
from asciimatics.widgets import Frame, Label, ListBox, Layout, Divider, Text, Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

from jinja2 import Environment, FileSystemLoader, Template

class PluginModel(object):
	"""docstring for PluginModel"""
	def __init__(self, d_plugin_conf=None):
		super(PluginModel, self).__init__()
		if d_plugin_conf != None:
			self.d_plugin_conf = d_plugin_conf
		else:
			self.d_plugin_conf = {'conf': {}}
	
	def add(self, key, value, part='conf'):
		self.d_plugin_conf[part][key] = value

	def add_dict(self, d_data, part='conf'):
		self.d_plugin_conf[part] = d_data

	def delete(self, key, part='conf'):
		del self.d_plugin_conf[part][key]

	def get_part_conf(self, part='conf'):
		return self.d_plugin_conf[part]

	def get_all_conf(self):
		return self.d_plugin_conf

class PluginConfView(Frame):
	"""docstring for PluginConfView"""
	def __init__(self, screen, plugin_data):
		super(PluginConfView, self).__init__(screen,
											screen.height * 2 // 3,
											screen.width * 2 // 3,
											hover_focus=True,
											title='Define Plugin configuration',
											reduce_cpu=True
											)
		self._plugin_data = plugin_data
		
		layout = Layout([100], fill_frame=True)
		self.add_layout(layout)
		layout.add_widget(Text('Hostname:', 'plugin_hostname'))
		layout.add_widget(Text('IP:', 'plugin_ip'))
		layout.add_widget(Text('Plugin log path:', 'plugin_log_path'))
		layout.add_widget(Text('InMan Server:', 'inman_server'))
		layout.add_widget(Text('Cluster Master Name:', 'cluster_master_name'))
		layout.add_widget(Text('Cluster Master IP:', 'cluster_master_ip'))
		layout.add_widget(Text('Cluster RADIUS name:', 'cluster_radius_name'))
		debug_choice = ListBox(4, [('Debug', 'logging.DEBUG'), ('Info', 'logging.INFO'), ('Warning', 'logging.WARNING'), ('Error', 'logging.ERROR'), ('Critical', 'logging.CRITICAL')], label='Agent debug level:', name='cluster_debug_level')
		layout.add_widget(debug_choice)

		layout2 = Layout([1, 1, 1, 1])
		self.add_layout(layout2)
		layout2.add_widget(Button('Next', self._next), 2)
		layout2.add_widget(Button('Quit', self._quit), 3)
		self.fix()

	def _next(self):
		self.save()
		self._plugin_data.add_dict(self.data)
		raise NextScene('Confirm conf creation')

	def reset(self):
		# Do standard reset to clear out form, then populate with new data.
		super(PluginConfView, self).reset()
		self.data = self._plugin_data.get_part_conf()

	@staticmethod
	def _quit():
		raise StopApplication('User pressed quit')

class CreateConfFileView(Frame):
	"""docstring for CreateConfFileView"""
	def __init__(self, screen, plugin_data):
		super(CreateConfFileView, self).__init__(screen,
											screen.height * 2 // 3,
											screen.width * 2 // 3,
											hover_focus=True,
											title='Create configuration file',
											reduce_cpu=True
											)
		self._plugin_data = plugin_data

		layout = Layout([100], fill_frame=True)
		self.add_layout(layout)
		layout.add_widget(Label(''))
		layout.add_widget(Label(''))
		layout.add_widget(Label('Confirm proceed to create configuration file for InMan Freeradius Cluster Plugin.'))

		layout2 = Layout([1, 1, 1, 1])
		self.add_layout(layout2)
		layout2.add_widget(Button('Proceed', self._proceed), 1)
		layout2.add_widget(Button('Previous', self._previous), 2)
		layout2.add_widget(Button('Quit', self._quit), 3)
		self.fix()

	def _proceed(self):
		d_conf = self._plugin_data.get_all_conf()
		print type(d_conf)
		print d_conf
		env = Environment(loader=FileSystemLoader('./templates'), extensions=['jinja2.ext.i18n'])
		env.list_templates(extensions=['tpl'])
		OTemplate = env.get_template('im_cluster_conf_freeradius.tpl')
		OTemplate.render(d_conf)
		fd = open(conf_file_dest, 'w')
		fd.write(OTemplate.render(d_conf))
		raise StopApplication('Proceed conf file creation')

	def _previous(self):
		raise NextScene('Conf Plugin')

	@staticmethod
	def _quit():
		raise StopApplication('User pressed quit')

def global_shortcuts(event):
	if isinstance(event, KeyboardEvent):
		c = event.key_code
		if c == -1:
			raise StopApplication('User pressed Esc')

def manage_plugin_conf(screen, scene):
	scenes = [
		Scene([PluginConfView(screen, plugin_data)], -1, name='Conf Plugin'),
		Scene([CreateConfFileView(screen, plugin_data)], -1, name='Confirm conf creation')
	]

	screen.play(scenes, stop_on_resize=True, start_scene=scene, unhandled_input=global_shortcuts)

plugin_data = PluginModel()

last_scene = None
if len(sys.argv) < 3:
	print 'Error :: CRITICAL :: No destination for InMan Freeradius Cluster plugin configuration file'
	sys.exit()

conf_file_dest = '{0}/{1}'.format(sys.argv[1], 'im_cluster_agent_freeradius.cfg')
plugin_data.add('cluster_master_name', sys.argv[2])
plugin_data.add('plugin_log_path', '/var/log/im_freeradius/cluster_agent.log')
while True:
	try:
		Screen.wrapper(manage_plugin_conf, catch_interrupt=True, arguments=[last_scene])
		sys.exit(0)
	except ResizeScreenError as e:
		last_scene = e.scene[Agent]