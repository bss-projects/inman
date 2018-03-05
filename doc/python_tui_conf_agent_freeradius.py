#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from asciimatics.event import Event, KeyboardEvent
from asciimatics.widgets import Frame, Label, ListBox, Layout, Divider, Text, Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

from jinja2 import Environment, FileSystemLoader, Template

class AgentModel(object):
	"""docstring for AgentModel"""
	def __init__(self, d_agent_conf=None):
		super(AgentModel, self).__init__()
		if d_agent_conf != None:
			self.d_agent_conf = d_agent_conf
		else:
			self.d_agent_conf = {'conf_agent': {}, 'server_info': {}}
	
	def add(self, part, key, value):
		self.d_agent_conf[part][key] = value

	def add_dict(self, part, d_data):
		self.d_agent_conf[part] = d_data

	def delete(self, part, key):
		del self.d_agent_conf[part][key]

	def get_part_conf(self, part):
		return self.d_agent_conf[part]

	def get_all_conf(self):
		return self.d_agent_conf

class AgentConfView(Frame):
	"""docstring for AgentConfView"""
	def __init__(self, screen, agent_data):
		super(AgentConfView, self).__init__(screen,
											screen.height * 2 // 3,
											screen.width * 2 // 3,
											hover_focus=True,
											title='Define Agent configuration',
											reduce_cpu=True
											)
		self._agent_data = agent_data
		
		layout = Layout([100], fill_frame=True)
		self.add_layout(layout)
		layout.add_widget(Text('Hostname:', 'agent_hostname'))
		layout.add_widget(Text('IP:', 'agent_ip'))
		layout.add_widget(Text('Agent name:', 'agent_name'))
		debug_choice = ListBox(4, [('Debug', 'logging.DEBUG'), ('Info', 'logging.INFO'), ('Warning', 'logging.WARNING'), ('Error', 'logging.ERROR'), ('Critical', 'logging.CRITICAL')], label='Agent debug level:', name='agent_debug_level')
		layout.add_widget(debug_choice)
		layout.add_widget(Text('Agent log path:', 'agent_log_path'))
		layout.add_widget(Text('RADIUS env path:', 'radius_env_path'))
		layout.add_widget(Text('RADIUS log path:', 'radius_log_path'))

		layout2 = Layout([1, 1, 1, 1])
		self.add_layout(layout2)
		layout2.add_widget(Button('Next', self._next), 2)
		layout2.add_widget(Button('Quit', self._quit), 3)
		self.fix()

	def _next(self):
		self.save()
		self._agent_data.add_dict('conf_agent', self.data)
		raise NextScene('Server Info')

	def reset(self):
		# Do standard reset to clear out form, then populate with new data.
		super(AgentConfView, self).reset()
		self.data = self._agent_data.get_part_conf('conf_agent')

	@staticmethod
	def _quit():
		raise StopApplication('User pressed quit')

class ServerInfoView(Frame):
	"""docstring for ServerInfoView"""
	def __init__(self, screen, agent_data):
		super(ServerInfoView, self).__init__(screen,
											screen.height * 2 // 3,
											screen.width * 2 // 3,
											hover_focus=True,
											title='Define Server info',
											reduce_cpu=True
											)
		self._agent_data = agent_data

		layout = Layout([100], fill_frame=True)
		self.add_layout(layout)
		layout.add_widget(Text('InMan server URL:', 'inman_server'))
		layout.add_widget(Text('Websocket server URL:', 'websocket_server'))
		layout.add_widget(Text('Websocket server port:', 'websocket_port'))
		layout.add_widget(Text('Websocket local log:', 'websocket_log_path'))
		debug_choice = ListBox(4, [('Debug', 'logging.DEBUG'), ('Info', 'logging.INFO'), ('Warning', 'logging.WARNING'), ('Error', 'logging.ERROR'), ('Critical', 'logging.CRITICAL')], label='Websocket debug level:', name='websocket_debug_level')
		layout.add_widget(debug_choice)

		layout2 = Layout([1, 1, 1, 1])
		self.add_layout(layout2)
		layout2.add_widget(Button('Finish', self._finish), 1)
		layout2.add_widget(Button('Previous', self._previous), 2)
		layout2.add_widget(Button('Quit', self._quit), 3)
		self.fix()

	def reset(self):
		# Do standard reset to clear out form, then populate with new data.
		super(ServerInfoView, self).reset()
		self.data = self._agent_data.get_part_conf('server_info')

	def _finish(self):
		self.save()
		self._agent_data.add_dict('server_info', self.data)
		raise NextScene('Confirm conf creation')

	def _previous(self):
		self.save()
		self._agent_data.add_dict('server_info', self.data)
		raise NextScene('Conf Agent')

	@staticmethod
	def _quit():
		raise StopApplication('User pressed quit')


class CreateConfFileView(Frame):
	"""docstring for CreateConfFileView"""
	def __init__(self, screen, agent_data):
		super(CreateConfFileView, self).__init__(screen,
											screen.height * 2 // 3,
											screen.width * 2 // 3,
											hover_focus=True,
											title='Create configuration file',
											reduce_cpu=True
											)
		self._agent_data = agent_data

		layout = Layout([100], fill_frame=True)
		self.add_layout(layout)
		layout.add_widget(Label(''))
		layout.add_widget(Label(''))
		layout.add_widget(Label('Confirm proceed to create configuration file for InMan Freeradius Agent.'))

		layout2 = Layout([1, 1, 1, 1])
		self.add_layout(layout2)
		layout2.add_widget(Button('Proceed', self._proceed), 1)
		layout2.add_widget(Button('Previous', self._previous), 2)
		layout2.add_widget(Button('Quit', self._quit), 3)
		self.fix()

	def _proceed(self):
		d_conf = self._agent_data.get_all_conf()
		env = Environment(loader=FileSystemLoader('./templates'), extensions=['jinja2.ext.i18n'])
		env.list_templates(extensions=['tpl'])
		OTemplate = env.get_template('im_agent_conf_freeradius.tpl')
		OTemplate.render(d_conf)
		fd = open(conf_file_dest, 'w')
		fd.write(OTemplate.render(d_conf))
		raise StopApplication('Proceed conf file creation')

	def _previous(self):
		raise NextScene('Server Info')

	@staticmethod
	def _quit():
		raise StopApplication('User pressed quit')


def global_shortcuts(event):
	if isinstance(event, KeyboardEvent):
		c = event.key_code
		if c == -1:
			raise StopApplication('User pressed Esc')

def manage_agent_conf(screen, scene):
	scenes = [
		Scene([AgentConfView(screen, agent_data)], -1, name='Conf Agent'),
		Scene([ServerInfoView(screen, agent_data)], -1, name='Server Info'),
		Scene([CreateConfFileView(screen, agent_data)], -1, name='Confirm conf creation')
	]

	screen.play(scenes, stop_on_resize=True, start_scene=scene, unhandled_input=global_shortcuts)

agent_data = AgentModel()

last_scene = None
if len(sys.argv) <= 1:
	print 'Error :: CRITICAL :: No destination for InMan Freeradius agent configuration file'
	sys.exit()
conf_file_dest = '{0}/{1}'.format(sys.argv[1], 'im_agent_freeradius.cfg')
agent_data.add_dict('server_info', {'websocket_port': '8080', 'websocket_log_path': '/var/log/im_freeradius/websocket.log'})
agent_data.add_dict('conf_agent', {'agent_log_path': '/var/log/im_freeradius/im.log', 'radius_env_path': '/etc/freeradius', 'radius_log_path': '/var/log/freeradius/radius.log'})

while True:
	try:
		Screen.wrapper(manage_agent_conf, catch_interrupt=True, arguments=[last_scene])
		sys.exit(0)
	except ResizeScreenError as e:
		last_scene = e.scene[Agent]
