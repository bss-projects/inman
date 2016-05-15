$(function()
{

	function onchallenge (session, method, extra) {
		if (method === "wampcra") {
			return autobahn.auth_cra.sign(Ckey, extra.challenge);
		}
	}

	function updateScrollToEnd(div_name){
		$(div_name).scrollTop($(div_name)[0].scrollHeight);
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
 
 		session.subscribe(uriTopic, onevent1);

		$('#file_view_log_freeradius').click(function() {

			unsubscribe(session);

			console.log('Call RPC readLogFreeradius');
			session.call('im.freeradius.file.log', []).then(
				function (res) {
					$('#frame_view_log_freeradius').empty();
					$('#frame_view_log_freeradius').append(res);
					updateScrollToEnd('#frame_view_log_freeradius');
					console.log("readLogFreeradius() success");
				},
				function (err) {
					console.log("readLogFreeradius() error:", err);
				}
			)
		});

		$('#live_view_log_freeradius').click(function() {
			$('#frame_view_log_freeradius').empty();
			unsubscribe(session);
			console.log(session);
			session.subscribe(uriTopic, onevent1);
		});

		function onevent1(args) {
			$('#frame_view_log_freeradius').append(args[0]+'</br>');
			updateScrollToEnd('#frame_view_log_freeradius')
			//	connection.close();
		}

	};
	
	connection.open();
});
