$(function()
{
	var Csession = null;

	function progress(percent, $element, info)
	{
		var progressBarWidth = percent * $element.width() / 100;
		$element.find('div').animate({ width: progressBarWidth }, 500).html(percent + "%&nbsp;");
	}

	function onchallenge (session, method, extra) {
		if (method === "wampcra") {
			return autobahn.auth_cra.sign(Ckey, extra.challenge);
		}
	}

	function unsubscribe(session)
	{
		for (var i = Object.keys(session._subscriptions).length - 1; i >= 0; i--) {
			sub_id = Object.keys(session._subscriptions)[i];
			if (session._subscriptions[sub_id][0])
			{
				session.unsubscribe(session._subscriptions[sub_id][0]);	
			};
		};
	}

	var connection = new autobahn.Connection({
		url: 'ws://'+urlCrossbar+':8080/ws',
		realm: realmCrossbar,
		authmethods: ["wampcra"],
		authid: Cuser,
		onchallenge: onchallenge}
	);

	connection.onopen = function (session) {
 
 		session.subscribe(uriTopicStatusSync, onevent1);
		Csession = session

		function onevent1(args) {

			console.log(args);
			progress_info = JSON.parse(args);
			progress(progress_info['progress'], $('#progressBar'), progress_info['msg']);
			//	connection.close();
		}

	};
	
	connection.open();

	$('#launch_sync').click(function() {
		console.log(Csession);
		$("#sync_div").show();
		Csession.publish(uriTopicSCP, ['{"hostname": "supervisor.server.lan", "distant_path_conf": "/appli/shinken/etc", "conf_file": "nagios.cfg", "agent_name": "SUP Server", "agent_ip": "127.0.0.1", "agent_rpc_port": "9000", "agent_connection_type": "RPC"}']);

	});

});
