[Plugin]
hostname = '{{ conf['plugin_hostname'] }}'
IP = '{{ conf['plugin_ip'] }}'
rpc_port = 8000

[Log]
filename = '{{ conf['plugin_log_path'] }}'
debug_level = '{{ conf['cluster_debug_level'] }}'

[Inman]
server = '{{ conf['inman_server'] }}'

[Cluster]
master_hostname = '{{ conf['cluster_master_name'] }}'
master_ip = '{{ conf['cluster_master_ip'] }}'
master_radius_name = '{{ conf['cluster_radius_name'] }}'
rpc_port = 9000