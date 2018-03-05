[Agent]
hostname = '{{ conf_agent['agent_hostname'] }}'
name = '{{ conf_agent['agent_name'] }}'
IP = '{{ conf_agent['agent_ip'] }}'
connection_type = 'RPC'
rpc_port = 9000

[Local conf]
client_filepath = '{{ conf_agent['radius_env_path'] }}'

[Log]
filename = '{{ conf_agent['agent_log_path'] }}'
debug_level = '{{ conf_agent['agent_debug_level'] }}'

[Inman]
server = '{{ server_info['inman_server'] }}'

[Websocket]
user = 'admin'
pass = 'pass'
router = '{{ server_info['websocket_server'] }}'
port = {{ server_info['websocket_port'] }}
realm = 'inman'
radius_log = '{{ conf_agent['radius_log_path'] }}'
uripubsub = 'im.freeradius.live.log'
urirpc_readfile_log = 'im.freeradius.file.log'
urirpc_listfile_log = 'im.freeradius.list.file.log'
log_file = '{{ server_info['websocket_log_path'] }}'
debug_level = '{{ server_info['websocket_debug_level'] }}'